import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}
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

    def add_mapping(self, pattern, pattern_format):
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text_block):
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text_block):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
