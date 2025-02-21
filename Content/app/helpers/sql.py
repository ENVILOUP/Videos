def clean_query(query: str) -> str:
    """ Convert a query string to a single line query string """
    return ' '.join(filter(lambda line: line, map(str.strip, query.split('\n'))))
