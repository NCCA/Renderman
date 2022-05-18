try:  # support either PyQt5 or 6
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import QPlainTextEdit, QToolTip, QWidget

    PySideVersion = 2
except ImportError:
    print("trying PySide6")
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import QPlainTextEdit, QToolTip, QWidget

    PySideVersion = 6

import sys


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        """init the class and setup dialog"""
        # Python 3 does inheritance differently to 2 so support both
        if sys.version_info.major == 3:
            super().__init__(parent)
        # python 2
        else:
            super(PlainTextEdit, self).__init__(parent)
        self.setMouseTracking(True)
        self.parent = parent

    def event(self, event):
        if event.type() is QEvent.ToolTip:
            helpEvent = QHelpEvent(event)
            pos = QPoint(helpEvent.pos())
            # pos.setX(pos.x() - self.viewportMargins().left())
            # pos.setY(pos.y() - self.viewportMargins().top())

            cursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.WordUnderCursor)
            QToolTip.setFont(self.font())
            QToolTip.showText(
                helpEvent.globalPos(), self.parent.help_text.get(cursor.selectedText())
            )
            return True
        else:
            return QPlainTextEdit.event(self, event)
