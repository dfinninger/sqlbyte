from collections import namedtuple
from enum import Enum, auto, unique


@unique
class Tokens(Enum):
    # Statement Verbs
    INSERT = auto()
    SELECT = auto()

    # Prepositions
    FROM = auto()
    INTO = auto()
    VALUES = auto()

    # Punctuation
    WILDCARD = auto()
    TERMINATOR = auto()
    OPEN_GROUP = auto()
    CLOSE_GROUP = auto()

    # Sometimes we just don't know what something is
    UNKNOWN = auto()


_KEYWORDS = {
    'insert': Tokens.INSERT,
    'select': Tokens.SELECT,
    'from': Tokens.FROM,
    'into': Tokens.INTO,
    'values': Tokens.VALUES,
    '*': Tokens.WILDCARD,
    ';': Tokens.TERMINATOR,
    '(': Tokens.OPEN_GROUP,
    ')': Tokens.CLOSE_GROUP,
}

_KEYWORDS_REV = {v: k for k, v in _KEYWORDS.items()}


TokenPair = namedtuple('TokenPair', ['token', 'keyword'])


def from_keyword(keyword: str) -> TokenPair:
    """Find a token, given a string

    Preforms a lookup on the token dict an supplies a token associated with the provided string.

    Args:
        keyword: Candidate string

    Returns:
        TokenPair - namedtuple of the form (token, keyword)
    """
    token = _KEYWORDS.get(keyword, Tokens.UNKNOWN)
    return TokenPair(token, keyword)


def from_token(token: int) -> TokenPair:
    """Find a keyword, given a token

    Preforms a reverse lookup on the token dict an supplies a string associated with the provided tpken.

    Args:
        token: Candidate token

    Returns:
        TokenPair - namedtuple of the form (token, keyword)
    """
    keyword = _KEYWORDS_REV.get(token, None)
    return TokenPair(token, keyword)
