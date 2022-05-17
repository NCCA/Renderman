#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PySide2.QtCore import *
    from PySide2.QtGui import (
        QColor,
        QFont,
        QFontMetrics,
        QStandardItem,
        QStandardItemModel,
        QTextCursor,
    )
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget

    PySideVersion = 2
except ImportError:
    print("trying PySide6")
    from PySide6.QtCore import QEvent, QFile, QObject, QSettings, QSize, Qt
    from PySide6.QtGui import (
        QColor,
        QFont,
        QFontMetrics,
        QStandardItem,
        QStandardItemModel,
        QTextCursor,
    )
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget

    PySideVersion = 6

import collections
import os
import sys
import xml.etree.ElementTree
from pathlib import Path

import PythonSyntax


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

        self.find_args_files()
        self.create_tree_view()
        self.ui.args_tree_view.clicked.connect(self.update_selection)
        self.ui.args_tree_view.setHeaderHidden(True)
        font = QFont()
        font.setFamily("Courier")
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(20)
        metrics = QFontMetrics(font)
        self.ui.rib.tabStopWidth = 2  # * metrics.width(" ")
        self.ui.rib.setFont(font)
        self.ui.python.setFont(font)
        self.ui.python.tabStopWidth = 2  # * metrics.width(" ")

        self.ui.rib.setFont(font)
        self.ui.python.setFont(font)

        self.ui.copy_python.pressed.connect(
            lambda: self.copy_to_clipboard(self.ui.python.toPlainText())
        )
        self.ui.copy_rib.pressed.connect(
            lambda: self.copy_to_clipboard(self.ui.rib.toPlainText())
        )

        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        self.resize(self.settings.value("size", QSize(1024, 800)))
        splitterSettings = self.settings.value("splitter")
        self.ui.main_splitter.restoreState(splitterSettings)
        self.ui.show()

    def closeEvent(self, event):
        self.settings.setValue("size", self.size())
        self.settings.setValue("splitter", self.ui.main_splitter.saveState())
        print("saving values", self.size())

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

    def debug(self):
        print("debug")

    def create_tree_view(self):
        self.data_model = QStandardItemModel()
        self.ui.args_tree_view.setModel(self.data_model)
        self.ui.args_tree_view.selectionModel().selectionChanged.connect(
            self.update_selection
        )

        # First we scan all the files to find the Core Shader Types and create empyty dictionary for them
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

    def generate_shader_text(self, path, name):
        self.ui.rib.clear()
        self.ui.python.clear()
        tree = xml.etree.ElementTree.parse(path).getroot()
        shader_type = tree.find("shaderType/tag").attrib.get("value")
        shader_type = "".join(
            shader_type[0].upper() + shader_type[1:]
        )  # First letter is capital bxdf to Bxdf
        # May also have Filter types such as LightFilter (lightFilter)
        shader_type = shader_type.replace("filter", "Filter")

        self.ui.rib.appendPlainText(f"{shader_type} {name}")
        self.ui.python.appendPlainText(f'ri.{shader_type}("{name}","id",')
        self.ui.python.appendPlainText("{")

        for p in tree.findall("param"):
            data_type = p.get("type")
            name = p.get("name")
            default_value = p.get("default")
            if default_value is None:
                default_value = "'No Value'"
            elif data_type == "string":
                default_value = "'" + default_value + "'"
            elif data_type == "float":
                default_value.replace(" ", ",")
                default_value = default_value.replace("f", "")
            self.ui.rib.appendPlainText(f'"{data_type} {name}" {default_value}')
            # need commas for python
            default_value = default_value.replace(" ", ",")
            self.ui.python.appendPlainText(
                f'\t"{data_type} {name}" : [{default_value}],'
            )
        # other data is in pages but add all of it
        page = tree.findall("page")
        for p in page:
            for param in p.findall("param"):
                data_type = param.get("type")
                name = param.get("name")
                default_value = param.get("default")
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
                self.ui.rib.appendPlainText(f'"{data_type} {name}"  [{default_value}]')
                # need commas for python
                default_value = default_value.replace(" ", ",")
                self.ui.python.appendPlainText(
                    f'\t"{data_type} {name}" : [{default_value}],'
                )

        # Close python dictionary to end
        self.ui.python.appendPlainText("})")
        self.ui.python.moveCursor(QTextCursor.Start)
        self.ui.rib.moveCursor(QTextCursor.Start)


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
