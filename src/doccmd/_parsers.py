"""
Custom parsers for doccmd.
"""

from typing import Optional

from beartype import beartype
from sybil.parsers.abstract.codeblock import AbstractCodeBlockParser
from sybil.parsers.myst.codeblock import (
    DirectiveInHTMLCommentLexer,
    DirectiveInPercentCommentLexer,
    DirectiveLexer,
    FencedCodeBlockLexer,
)
from sybil.typing import Evaluator


@beartype
class MystCodeBlockParser(AbstractCodeBlockParser):
    """
    A custom MyST code block parser that extends sybil's CodeBlockParser.

    This parser recognizes the same directives as sybil's CodeBlockParser,
    plus the MyST ``code-cell`` directive which is commonly used in Jupyter
    notebooks and MyST markdown files.

    :param language:
        The language that this parser should look for.

    :param evaluator:
        The evaluator to use for evaluating code blocks in the specified language.
    """

    def __init__(
        self,
        language: Optional[str] = None,
        evaluator: Optional[Evaluator] = None,
    ) -> None:
        """
        Initialize the parser with support for code-cell directive.
        """
        super().__init__(
            [
                FencedCodeBlockLexer(
                    language=r".+",
                    mapping={"language": "arguments", "source": "source"},
                ),
                DirectiveLexer(
                    directive=r"(sourcecode|code-block|code-cell|code)",
                    arguments=".+",
                ),
                DirectiveInPercentCommentLexer(
                    directive=r"(invisible-)?code(-block|-cell)?",
                    arguments=".+",
                ),
                DirectiveInHTMLCommentLexer(
                    directive=r"(invisible-)?code(-block|-cell)?",
                    arguments=".+",
                ),
            ],
            language,
            evaluator,
        )
