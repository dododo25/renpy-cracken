import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], '..')))

import argparse
import cracken
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main(path, recursive, clear, prettify):
    archive_files = []
    regular_files = []

    def prepare_file(path):
        if cracken.is_archive(path):
            archive_files.append(path)
        elif cracken.is_file(path):
            regular_files.append(path)

    cracken.collect_files(os.path.abspath(path), prepare_file)

    if not len(regular_files) and not len(archive_files):
        logger.warning('no files were found')
        return

    while archive_files:
        path = archive_files.pop()

        logger.info('trying to extract %s' % path)
        cracken.process_archive_file(path, recursive, prepare_file if recursive else None)

        if clear:
            os.remove(path)

    for path in regular_files:
        try:
            logger.info('trying to deserialize %s' % path)
            cracken.process_file(path, prettify)
        except (ModuleNotFoundError, AttributeError) as e:
            logger.critical(e)
            raise e

    logger.info('done')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cracken.py', 
                                     description='Decompile RenPy files and extract additional files from a RenPy archive')

    parser.add_argument('-r', '--recursive', help='Process files that were extracted from archives', action='store_true')
    parser.add_argument('-c', '--clear', help='Delete archive files after they were processed', action='store_true')
    parser.add_argument('-p', '--prettify', help='Try to make Python code snippets more pretty', action='store_true')
    parser.add_argument('file', help='Path to file\\folder that this program should process')

    args = parser.parse_args()

    main(args.file, args.recursive, args.clear, args.prettify)
