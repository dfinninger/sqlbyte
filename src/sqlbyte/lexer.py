"""
lexer.py

Tools for preforming lexical analysis.
"""
from src.sqlbyte import tokens


def tokenize(instr: str) -> list:
    """Takes a string and splits it into a list of tokens.TokenPairs

    Args:
        instr: input string
    Returns:
        list of tokens.TokenPairs
    """
    candidates = instr.split()
    # TODO(dfinninger): Handle paren groups correctly
    return [_get_tokens(item) for item in candidates]


def _get_tokens(candidate):
    candidate.lower()
    return tokens.from_keyword(candidate)
