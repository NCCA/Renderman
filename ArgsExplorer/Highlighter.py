import re
import sys

try:  # support either PyQt5 or 6
    from PySide2.QtCore import Qt
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

    PySideVersion = 2
except ImportError:
    print("trying PySide6")
    from PySide6.QtCore import Qt
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *

    PySideVersion = 6



class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}
        # define pattern rule #1: ri.XXX
        class_format = QTextCharFormat()
        class_format.setForeground(Qt.GlobalColor.blue)
        class_format.setFontWeight(QFont.Weight.Bold)
        pattern = r"^ri.[^\(]*"
        self._mapping[pattern] = class_format
        # keywords
        keywords_format = QTextCharFormat()
        keywords_format.setForeground(Qt.GlobalColor.green)
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

    def add_mapping(self, pattern, pattern_format):
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text_block):
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text_block):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
