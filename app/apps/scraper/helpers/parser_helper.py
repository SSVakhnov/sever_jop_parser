__all__ = [
    'get_safe_html_text'
]


def get_safe_html_text(variable):
    if variable:
        variable = variable.text
    return variable
