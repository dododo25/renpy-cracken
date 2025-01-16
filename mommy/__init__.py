import yapf

config = {
    'BASED_ON_STYLE': 'pep8', 
    'INDENT_WIDTH': 4, 
    'CONTINUATION_ALIGN_STYLE': 'fixed', 
    'CONTINUATION_INDENT_WIDTH': 4,
    'BLANK_LINES_BETWEEN_TOP_LEVEL_IMPORTS_AND_VARIABLES': 1,
    'JOIN_MULTIPLE_LINES': False,
    'BLANK_LINES_AROUND_TOP_LEVEL_DEFINITION': 1
}

def clean(code: str) -> str:
    formatted = yapf.yapf_api.FormatCode(code, style_config=config)[0]

    if formatted[-1] == '\n':
        return formatted[:-1]
    
    return formatted
