import re
from typing import Dict, Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class Highlighter(QSyntaxHighlighter):
    """
    A custom syntax highlighter for RenderMan shader language.

    Highlights RenderMan function calls, keywords, data types, numbers,
    brackets, and quotes with specific color schemes.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Initialize the Highlighter with predefined syntax highlighting patterns.

        Sets up color formatting rules for:
        - RenderMan functions (ri.*) and plugin names
        - Language keywords (color, int, float, etc.)
        - Brackets and quotes
        - Numeric literals

        Args:
            parent: Optional parent QObject for memory management.
        """
        super().__init__(parent)
        self._mapping: Dict[str, QTextCharFormat] = {}

        # define pattern rule #1: ri.XXX and Plugin names
        shader_format = QTextCharFormat()
        shader_format.setForeground(QColor(83, 150, 206))
        shader_format.setFontWeight(QFont.Weight.Bold)
        pattern = r"(^ri.[^\(]*)|(Bxdf |(Pattern )|SampleFilter |DisplayFilter |Displaydriver |Projection|Integrator|Displacement)|(Light )|(LightFilter )"
        self._mapping[pattern] = shader_format

        # keywords
        keywords_format = QTextCharFormat()
        keywords_format.setForeground(QColor(206, 145, 120))
        keywords_format.setFontWeight(QFont.Weight.Bold)
        # \\b \\b matches whole word boundary
        pattern = [
            "\\bcolor\\b",
            "\\bint\\b",
            "\\bfloat\\b",
            "\\bnormal\\b",
            "\\bstring\\b",
            "\\bbxdf\\b",
            "\\bmatrix\\b",
            "\\blightfilter\\b",
            "\\bpoint\\b",
            "\\bvector\\b",
        ]
        for p in pattern:
            self._mapping[p] = keywords_format

        # Brackets and Quotes
        brackets_format = QTextCharFormat()
        brackets_format.setForeground(QColor(254, 240, 0))
        shader_format.setFontWeight(QFont.Weight.Bold)
        pattern = r"\(|\)|\[|\]|\{|\|\'|\"|\,\}"
        self._mapping[pattern] = brackets_format

        # Numbers 181,206,168
        numbers_format = QTextCharFormat()
        numbers_format.setForeground(QColor(181, 206, 168))
        numbers_format.setFontWeight(QFont.Weight.Bold)
        pattern = r"[0-9]+"
        self._mapping[pattern] = numbers_format

    def add_mapping(self, pattern: str, pattern_format: QTextCharFormat) -> None:
        """
        Add a custom syntax highlighting rule.

        Args:
            pattern: A regex pattern string to match in the text.
            pattern_format: The QTextCharFormat to apply to matched text.
        """
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text_block: str) -> None:
        """
        Apply syntax highlighting to a single line of text.

        Iterates through all registered patterns and applies the corresponding
        formatting to matching text segments in the given line.

        Args:
            text_block: The line of text to highlight.
        """
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text_block):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
