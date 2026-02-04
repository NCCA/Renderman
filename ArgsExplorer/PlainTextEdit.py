try:  # support either PyQt5 or 6
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import QPlainTextEdit, QToolTip, QWidget

    PySideVersion = 2
except ImportError:
    print("trying PySide6")
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import QPlainTextEdit, QToolTip

    PySideVersion = 6


class PlainTextEdit(QPlainTextEdit):
    """
    Need to override the simple QPlainTextEdit so we can capture the
    ToolTip event and create custom ones from us.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.parent = parent
        self.setStyleSheet("background-color: rgb(30,30,30);color : rgb(250,250,250);")

    def event(self, event):
        """going to re-implement the event for tool tips then
        pass on to parent if not a tool tip
        """
        if event.type() is QEvent.ToolTip:
            # Grab the help event and get the position
            if PySideVersion == 6 :
                helpEvent = QHelpEvent(event)
                pos = QPoint(helpEvent.pos())

            else :
                helpEvent= event #QHelpEvent(event,event.pos(),event.globalPos())
                pos = QPoint(helpEvent.pos())
    
            # find text under the cursos and lookup
            cursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.WordUnderCursor)
            # help text is not the best, form to HTML and paragraph
            raw_text = self.parent.help_text.get(cursor.selectedText())
            if raw_text is not None:
                raw_text = raw_text.replace(". ", ".<br/><p/>")
                help_text = f"<html><p/>{raw_text}</html>"

                QToolTip.showText(helpEvent.globalPos(), help_text)

            return True
        else:
            return QPlainTextEdit.event(self, event)
