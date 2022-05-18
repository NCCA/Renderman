#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import (
        QApplication,
        QFontDialog,
        QMainWindow,
        QMenu,
        QStatusBar,
        QWidget,
    )

    PySideVersion = 2
except ImportError:
    print("trying PySide6")
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import (
        QApplication,
        QFontDialog,
        QMainWindow,
        QMenu,
        QStatusBar,
        QWidget,
    )

    PySideVersion = 6

import collections
import os
import sys
import xml.etree.ElementTree
from pathlib import Path

from PlainTextEdit import PlainTextEdit


class ArgsExplorer(QMainWindow):
    def __init__(self, rmantree, parent=None):
        """init the class and setup dialog"""
        # Python 3 does inheritance differently to 2 so support both
        if sys.version_info.major == 3:
            super().__init__(parent)
        # python 2
        else:
            super(ArgsExplorer, self).__init__(parent)
        loader = QUiLoader()
        self.rmantree = rmantree
        file = QFile("./ui/form.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        self.setWindowTitle("Renderman Argument Explorer")
        self.tab_size = 2
        self.help_text = dict()
        self.find_args_files()
        self.create_tree_view()
        self.setMouseTracking(True)

        self.python = PlainTextEdit(self)
        self.ui.python_layout.insertWidget(0, self.python)
        self.rib = PlainTextEdit(self)
        self.ui.rib_layout.insertWidget(0, self.rib)

        self.ui.copy_python.pressed.connect(
            lambda: self.copy_to_clipboard(self.python.toPlainText())
        )
        self.ui.copy_rib.pressed.connect(
            lambda: self.copy_to_clipboard(self.rib.toPlainText())
        )
        self.ui.expand_all.stateChanged.connect(
            lambda state: self.ui.args_tree_view.expandAll()
            if state
            else self.ui.args_tree_view.collapseAll()
        )

        self.loadSettings()
        self.create_menu_bar()
        self.ui.show()

    def loadSettings(self):
        """Load in the setting.ini file if exists to setup our env from last time"""
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        self.resize(self.settings.value("size", QSize(1024, 800)))
        splitterSettings = self.settings.value("splitter")
        self.ui.main_splitter.restoreState(splitterSettings)
        self.ui.expand_all.setChecked(self.settings.value("expand_all", type=bool))
        self.settings.beginGroup("Font")

        font = QFont(
            self.settings.value("font-name", type=str),
            self.settings.value("font-size", type=int),
            self.settings.value("font-weight", type=int),
            self.settings.value("font-italic", type=bool),
        )
        self.settings.endGroup()
        self.set_editor_fonts(font)

    def closeEvent(self, event):
        """on close we save to settings.ini using QSettings"""
        self.settings.setValue("size", self.size())
        self.settings.setValue("splitter", self.ui.main_splitter.saveState())
        self.settings.setValue("expand_all", self.ui.expand_all.isChecked())
        self.settings.beginGroup("Font")
        font = self.rib.font()
        self.settings.setValue("font-name", font.family())
        self.settings.setValue("font-size", font.pointSize())
        self.settings.setValue("font-weight", font.weight())
        self.settings.setValue("font-italic", font.italic())
        self.settings.endGroup()

    def create_menu_bar(self):
        # export menu
        menu = self.menuBar()
        export_menu = QMenu("&File", self)
        export_menu.addAction("Export")
        menu.addMenu(export_menu)
        # font menu
        font_menu = QMenu("&Font", self)
        change_font_action = QAction("Change Font", self)
        font_menu.addAction(change_font_action)
        change_font_action.triggered.connect(self.change_font)
        menu.addMenu(font_menu)

    def change_font(self):
        (ok, font) = QFontDialog.getFont(QFont(), self)
        if ok:
            self.set_editor_fonts(font)

    def set_editor_fonts(self, font):
        metrics = QFontMetrics(font)
        self.rib.setTabStopDistance(
            QFontMetricsF(self.rib.font()).horizontalAdvance(" ") * self.tab_size
        )
        self.python.setTabStopDistance(
            QFontMetricsF(self.python.font()).horizontalAdvance(" ") * self.tab_size
        )
        self.rib.setFont(font)
        self.python.setFont(font)

    def copy_to_clipboard(self, text):

        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(text, mode=clipboard.Clipboard)

    def update_selection(self):
        index = self.ui.args_tree_view.currentIndex()
        # grab the full file path
        path = self.ui.args_tree_view.model().data(index, 1)
        name = self.ui.args_tree_view.model().data(index, 0)
        if path is not None:
            self.generate_shader_text(path, name)

    def find_args_files(self):
        self.arg_files = list(Path(self.rmantree).glob("**/*.args"))
        self.statusBar().showMessage(f"Found {len(self.arg_files)} argument files")

    def create_tree_view(self):
        self.data_model = QStandardItemModel()
        self.ui.args_tree_view.setModel(self.data_model)
        self.ui.args_tree_view.selectionModel().selectionChanged.connect(
            self.update_selection
        )

        # First we scan all the files to find the Core Shader Types and create empty dictionary for them
        shader_types = dict()
        for arg_file in self.arg_files:
            tree = xml.etree.ElementTree.parse(arg_file).getroot()
            shader_type = tree.find("shaderType/tag").attrib.get("value")
            shader_type = "".join(shader_type[0].upper() + shader_type[1:])
            shader_types[shader_type] = list()
        # Now we have the core types add the actual shaders to them
        for arg_file in self.arg_files:
            tree = xml.etree.ElementTree.parse(arg_file).getroot()
            shader_type = tree.find("shaderType/tag").attrib.get("value")
            shader_type = "".join(shader_type[0].upper() + shader_type[1:])
            shader_types[shader_type].append([arg_file.stem, arg_file])

        for shader in shader_types:
            row = QStandardItem(shader)
            row.setEditable(False)

            for name, full_path in shader_types[shader]:
                item = QStandardItem(name)
                item.setData(full_path, 1)
                item.setEditable(False)
                row.appendRow(item)
            self.data_model.appendRow(row)
        # setup the tree view
        self.ui.args_tree_view.clicked.connect(self.update_selection)
        self.ui.args_tree_view.setHeaderHidden(True)
        self.ui.args_tree_view.setFocus()
        if self.ui.expand_all.isChecked():
            self.ui.args_tree_view.expandAll()
        else:
            self.ui.args_tree_view.collapseAll()
        self.ui.args_tree_view.setCurrentIndex(
            self.ui.args_tree_view.model().index(0, 0)
        )

    def generate_shader_text(self, path, name):
        self.rib.clear()
        self.python.clear()
        self.help_text.clear()
        tree = xml.etree.ElementTree.parse(path).getroot()
        shader_type = tree.find("shaderType/tag").attrib.get("value")
        shader_type = "".join(
            shader_type[0].upper() + shader_type[1:]
        )  # First letter is capital bxdf to Bxdf
        # May also have Filter types such as LightFilter (lightFilter)
        shader_type = shader_type.replace("filter", "Filter")

        self.rib.appendPlainText(f"{shader_type} {name}")
        self.python.appendPlainText(f'ri.{shader_type}("{name}","id",')
        self.python.appendPlainText("{")

        for p in tree.findall("param"):
            data_type = p.get("type")
            name = p.get("name")
            help_text = p.find(f"help")
            if help_text is not None:
                htext = help_text.text
                htext.lstrip()
            else:
                htext = "No Help for this item"
            self.help_text[name] = htext

            default_value = p.get("default")
            if default_value is None:
                default_value = "'No Value'"
            elif data_type == "string":
                default_value = "'" + default_value + "'"
            elif data_type == "float":
                default_value.replace(" ", ",")
                default_value = default_value.replace("f", "")
            self.rib.appendPlainText(f'"{data_type} {name}" {default_value}')
            # need commas for python
            default_value = default_value.replace(" ", ",")
            self.python.appendPlainText(f'\t"{data_type} {name}" : [{default_value}],')
        # other data is in pages but add all of it
        page = tree.findall("page")
        for p in page:
            for param in p.findall("param"):
                data_type = param.get("type")
                name = param.get("name")
                default_value = param.get("default")
                help_text = param.find(f"help")
                if help_text is not None:
                    htext = help_text.text
                    htext.lstrip()
                else:
                    htext = "No Help for this item"
                self.help_text[name] = htext

                if default_value == None:
                    default_value = "'No Value'"  # sometimes there is no default
                elif data_type == "string":
                    default_value = (
                        "'" + default_value + "'"
                    )  # strings need to be quoted
                elif data_type == "float":
                    default_value = default_value.replace(
                        "f", ""
                    )  # seems some floats us 0.0f
                self.rib.appendPlainText(f'"{data_type} {name}"  [{default_value}]')
                # need commas for python
                default_value = default_value.replace(" ", ",")
                self.python.appendPlainText(
                    f'\t"{data_type} {name}" : [{default_value}],'
                )

        # Close python dictionary to end
        self.python.appendPlainText("})")
        self.python.moveCursor(QTextCursor.Start)
        self.rib.moveCursor(QTextCursor.Start)


if __name__ == "__main__":
    rmantree = os.environ.get("RMANTREE")
    if rmantree is None:
        print("RMANTREE not set exiting")
        sys.exit(os.EX_CONFIG)

    app = QApplication(sys.argv)
    app.setOrganizationName("NCCA")
    app.setOrganizationDomain("ncca.bournemouth.ac.uk")
    app.setApplicationName("ArgsExplorer")
    window = ArgsExplorer(rmantree)
    window.show()
    app.exec()
