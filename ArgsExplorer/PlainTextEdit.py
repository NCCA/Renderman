from typing import Any, Optional

from PySide6.QtCore import QEvent, QObject, QPoint
from PySide6.QtGui import QHelpEvent, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QToolTip


class PlainTextEdit(QPlainTextEdit):
    """
    A custom QPlainTextEdit that displays context-sensitive tooltips.

    Overrides the standard QPlainTextEdit to intercept ToolTip events and
    display custom tooltips based on the word under the cursor. The tooltips
    are looked up from a parent object's help_text dictionary.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Initialize the PlainTextEdit widget.

        Enables mouse tracking and applies dark theme styling to the editor.

        Args:
            parent: Optional parent QObject for widget hierarchy and memory management.
        """
        super().__init__(parent)
        self.setMouseTracking(True)
        self.parent: Optional[QObject] = parent
        self.setStyleSheet("background-color: rgb(30,30,30);color : rgb(250,250,250);")

    def event(self, event: QEvent) -> bool:
        """
        Override event handling to provide custom tooltips.

        Intercepts ToolTip events and displays context-sensitive help text
        for the word under the cursor. If the word is found in the parent's
        help_text dictionary, a formatted HTML tooltip is shown. Other events
        are passed to the parent class for normal processing.

        Args:
            event: The QEvent to process.

        Returns:
            True if a tooltip was displayed (ToolTip event), False otherwise.
        """
        if event.type() is QEvent.ToolTip:
            # Grab the help event and get the position
            helpEvent: QHelpEvent = QHelpEvent(event)
            pos: QPoint = QPoint(helpEvent.pos())

            # find text under the cursor and lookup
            cursor: QTextCursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.WordUnderCursor)

            # help text is not the best, form to HTML and paragraph
            selected_word: str = cursor.selectedText()
            raw_text: Optional[str] = self.parent.help_text.get(selected_word) if self.parent else None

            if raw_text is not None:
                raw_text = raw_text.replace(". ", ".<br/><p/>")
                help_text: str = f"<html><p/>{raw_text}</html>"
                QToolTip.showText(helpEvent.globalPos(), help_text)

            return True
        else:
            return QPlainTextEdit.event(self, event)
