from app.helpers.sql import clean_query


def test_clean_query_single_line():
    query = "SELECT * FROM table"
    expected = "SELECT * FROM table"
    assert clean_query(query) == expected


def test_clean_query_multiple_lines():
    query = """
    SELECT *
    FROM table
    WHERE column = 'value'
    """
    expected = "SELECT * FROM table WHERE column = 'value'"
    assert clean_query(query) == expected


def test_clean_query_with_extra_spaces():
    query = """
    SELECT  *
    FROM    table
    WHERE   column = 'value'
    """
    expected = "SELECT  * FROM    table WHERE   column = 'value'"
    assert clean_query(query) == expected

def test_clean_query_with_spaces_in_string():
    query = """
    SELECT  *
    FROM    table
    WHERE   title LIKE '% - %'
    """
    expected = "SELECT  * FROM    table WHERE   title LIKE '% - %'"
    assert clean_query(query) == expected

def test_clean_query_with_two_consecutive_spaces_in_string():
    query = """
    SELECT  *
    FROM    table
    WHERE   title LIKE '%  - %'
    """
    expected = "SELECT  * FROM    table WHERE   title LIKE '%  - %'"
    assert clean_query(query) == expected
