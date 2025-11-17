"""
Custom parsers for doccmd.
"""

from beartype import beartype
from sybil.parsers.abstract.codeblock import AbstractCodeBlockParser
from sybil.parsers.markdown.lexers import (
    DirectiveInHTMLCommentLexer,
    FencedCodeBlockLexer,
)
from sybil.parsers.myst.lexers import (
    DirectiveInPercentCommentLexer,
    DirectiveLexer,
)
from sybil.typing import Evaluator


@beartype
class MystCodeBlockParser(AbstractCodeBlockParser):  # pylint: disable=abstract-method
    """
    A custom MyST code block parser that extends Sybil CodeBlockParser.

    This parser recognizes the same directives as Sybil CodeBlockParser,
    plus the MyST ``code-cell`` directive which is commonly used in Jupyter
    notebooks and MyST markdown files.

    :param language:
        The language that this parser should look for.

    :param evaluator:
        The evaluator to use for evaluating code blocks in the
        specified language.
    """

    def __init__(
        self,
        language: str | None = None,
        evaluator: Evaluator | None = None,
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
