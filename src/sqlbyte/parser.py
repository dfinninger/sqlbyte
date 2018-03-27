"""
parser.py

Tools for parsing token lists into structured grammars.
"""
import itertools

from src.sqlbyte.tokens import Tokens

_SELECT_ERROR_PREAMBLE = 'Malformed SELECT statement'
_INSERT_ERROR_PREAMBLE = 'Malformed INSERT statement'


class ParserValidationError(Exception):
    pass


def validate(token_list: list):
    """
    validate

    Validates that a token list is grammatically correct.

    param token_list: list of tokens
    raises: ParserValidationError is issues arise
    """
    if not token_list:
        return []

    # Copy the token list so that we can be destructive
    tl = list(token_list)
    statement_type = tl[0].token

    if statement_type == Tokens.SELECT:
        _validate_select_statement(tl)
    elif statement_type == Tokens.INSERT:
        _validate_insert_statement(tl)
    else:
        raise(ParserValidationError(f'Bad statement type: {statement_type}'))


def _validate_select_statement(token_list):
    """
    validates a select statement

    Select statements are of the form:

        SELECT select_list FROM table_name

        Where:
            select_list is either "*" or "a, b, c, ..."
            table_name is the table representation (usually a simple string)
    """
    try:
        assert Tokens.SELECT == token_list.pop(0)
    except AssertionError:
        raise(ParserValidationError(f'{_SELECT_ERROR_PREAMBLE}: does not start with "INSERT INTO".'))

    # There are a variable number of arguments here, so we'll loop until they are consumed
    fields = []
    while len(token_list) > 0:
        if token_list[0] == Tokens.FROM:
            break

        item = token_list.pop(0)
        fields.append(item)

        if item == Tokens.WILDCARD:
            break
    else:
        raise(ParserValidationError(f'{_SELECT_ERROR_PREAMBLE}: parser reached end of token list prematurely.'))

    # Ensure that we have at least "FROM something" left in the token list
    if len(token_list) <= 1:
        raise(ParserValidationError(f'{_SELECT_ERROR_PREAMBLE}: not enough tokens for FROM clause.'))


def _validate_insert_statement(token_list):
    """
    validates an insert statement

    Insert statements are of the form:

        INSERT INTO table_name (a, b, c, ...) VALUES (x, y, z, ...)

        Where:
            a/b/c represent column names
            x/y/z represent values for the row
    """
    if Tokens.INSERT != token_list.pop(0):
        raise(ParserValidationError(f'{_INSERT_ERROR_PREAMBLE}: does not start with "INSERT INTO"'))

    if Tokens.INTO != token_list.pop(0):
        raise(ParserValidationError(f'{_INSERT_ERROR_PREAMBLE}: does not start with "INSERT INTO"'))

    table = token_list.pop(0)

    if not Tokens.VALUES == token_list[0]:
        token_list = _validate_group(token_list)

    if Tokens.VALUES != token_list.pop(0):
        raise(ParserValidationError(f'{_INSERT_ERROR_PREAMBLE}: missing VALUES keyword'))

    _validate_group(token_list)

def _validate_group(token_list):
    if Tokens.OPEN_GROUP != token_list.pop(0):
        raise(ParserValidationError(f'Missing "{Tokens.OPEN_GROUP}" at start of group'))

    group = itertools.takewhile(lambda x: x != Tokens.CLOSE_GROUP, token_list)
    token_list = itertools.dropwhile(lambda x: x != Tokens.CLOSE_GROUP, token_list)

    if not group:
        raise(ParserValidationError(f'Empty group'))

    if Tokens.CLOSE_GROUP != token_list.pop(0):
        raise(ParserValidationError(f'Missing "{Tokens.CLOSE_GROUP}" at end of group'))

    return token_list


def parse(token_list: list):
    """"
    parse

    parses a token list into a command object
    """
    # TODO(dfinninger): Implement a command object
    pass