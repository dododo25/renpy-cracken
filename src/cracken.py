import argparse
import cracken
import logging
import os
import traceback

log_filename = 'logs/cracken.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)4s - %(filename)s:%(lineno)s - %(message)s')

def clean_lines(count):
    if count < 1:
        raise ValueError()

    if count > 1:
        print('\033[' + str(count - 1) + 'A', end='')

    print(('\033[2K\n') * count + '\033[' + str(count) + 'A', end='')

def main(path, recursive, clear, prettify, skip_error):
    archive_files = []
    regular_files = []

    def prepare_file(path):
        if cracken.is_archive(path):
            archive_files.append(path)
        elif cracken.is_file(path):
            regular_files.append(path)

    cracken.collect_files(os.path.abspath(path), prepare_file)

    if not len(regular_files) and not len(archive_files):
        print('No files were found!')
        return

    while archive_files:
        path = archive_files.pop()

        print('Trying to extract %s' % path, end='')
        cracken.process_archive_file(path, recursive, prepare_file if recursive else None)
        clean_lines(1)

        if clear:
            os.remove(path)

    for path in regular_files:
        try:
            print('Trying to deserialize %s' % path, end='')
            cracken.process_file(path, prettify)
            clean_lines(1)
        except (ModuleNotFoundError, AttributeError) as e:
            print()

            if skip_error:
                raise e

            print(type(e).__name__ + ':', e)

    print('All done, bye 👋')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cracken.py', 
                                     description='Decompile RenPy files and extract additional files from a RenPy archive')

    parser.add_argument('-r', '--recursive',  help='Process files that were extracted from archives',   action='store_true')
    parser.add_argument('-c', '--clear',      help='Delete archive files after they were processed',    action='store_true')
    parser.add_argument('-p', '--prettify',   help='Try to make Python code snippets more pretty',      action='store_true')
    parser.add_argument('-s', '--skip-error', help='Execution will not be stopped if an error happens', action='store_true')
    parser.add_argument('file', help='Path to file\\folder that this program should process')

    args = parser.parse_args()

    main(args.file, args.recursive, args.clear, args.prettify, args.skip_error)
