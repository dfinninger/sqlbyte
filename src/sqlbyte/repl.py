from prompt_toolkit import prompt_async
from pygments.lexers.sql import SqlLexer

from src.sqlbyte import parser
from src.sqlbyte import lexer
from src.sqlbyte.tokens import Tokens


async def run():
    while True:
        result = await prompt_async('repl> ', patch_stdout=True, lexer=SqlLexer)

        tokens = lexer.tokenize(result)

        try:
            parser.validate(tokens)
        except parser.ParserValidationError as e:
            print(f'Error: {e}')
        else:
            print(tokens)

        if tokens[0] == Tokens.INSERT:
            print(tokens)
