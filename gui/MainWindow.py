import logging
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt

from common import Storage, Character
from core.composor import get_character_svg_at_index, get_character_svgs_in_range
from .utils import render_svg_to_view_from_str, render_svg_to_view, get_qt_svg_item
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, config: Storage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # uic.loadUi("gui/MainWindow.ui", self)
        self.setupUi(self)
        # self.inputTextEdit = self.findChild(QtWidgets.QTextEdit, "inputTextEdit")
        # self.doneStrokeColorInput = self.findChild(
        #     QtWidgets.QLineEdit, "doneStrokeColorInput"
        # )
        # self.newStrokeColorInput = self.findChild(
        #     QtWidgets.QLineEdit, "newStrokeColorInput"
        # )
        # self.undoneStrokeColorInput = self.findChild(
        #     QtWidgets.QLineEdit, "undoneStrokeColorInput"
        # )
        # self.gridColorInput1 = self.findChild(QtWidgets.QLineEdit, "gridColorInput1")
        # self.gridColorInput2 = self.findChild(QtWidgets.QLineEdit, "gridColorInput2")
        # self.gridDashLenInput1 = self.findChild(
        #     QtWidgets.QLineEdit, "gridDashLenInput1"
        # )
        # self.gridDashLenInput2 = self.findChild(
        #     QtWidgets.QLineEdit, "gridDashLenInput2"
        # )
        # self.gridDashSpaceInput1 = self.findChild(
        #     QtWidgets.QLineEdit, "gridDashSpaceInput1"
        # )
        # self.gridDashSpaceInput2 = self.findChild(
        #     QtWidgets.QLineEdit, "gridDashSpaceInput2"
        # )
        # self.gridWidthInput1 = self.findChild(QtWidgets.QLineEdit, "gridWidthInput1")
        # self.gridWidthInput2 = self.findChild(QtWidgets.QLineEdit, "gridWidthInput2")
        # self.gridVisibility1 = self.findChild(QtWidgets.QCheckBox, "gridVisibility1")
        # self.gridVisibility2 = self.findChild(QtWidgets.QCheckBox, "gridVisibility2")
        # self.borderColorInput = self.findChild(QtWidgets.QLineEdit, "borderColorInput")
        # self.borderWidthInput = self.findChild(QtWidgets.QLineEdit, "borderWidthInput")
        # self.borderVisibility = self.findChild(QtWidgets.QCheckBox, "borderVisibility")

        # self.curCharComboBox = self.findChild(QtWidgets.QComboBox, "curCharComboBox")
        # self.strokePreview = self.findChild(QtWidgets.QGraphicsView, "strokePreview")
        # self.curStrokeComboBox = self.findChild(
        #     QtWidgets.QComboBox, "curStrokeComboBox"
        # )
        # self.totalStrokeLabel = self.findChild(QtWidgets.QLabel, "totalStrokeLabel")
        # self.updatePreviewBtn = self.findChild(
        #     QtWidgets.QPushButton, "updatePreviewBtn"
        # )
        
        # self.outputDirInput = self.findChild(QtWidgets.QLineEdit, "outputDirInput")
        # self.outputDirSelectBtn = self.findChild(
        #     QtWidgets.QPushButton, "outputDirSelectBtn"
        # )
        # self.progressBar = self.findChild(QtWidgets.QProgressBar, "progressBar")
        # self.startBtn = self.findChild(QtWidgets.QPushButton, "startBtn")
        # self.closeBtn = self.findChild(QtWidgets.QPushButton, "closeBtn")

        self.previewSvgItem = None
        self.logger = logging.getLogger("AppLogger")

        self.config = config

        self.load_config()

        self.doneStrokeColorInput.textChanged.connect(self.update_done_stroke_color)
        self.newStrokeColorInput.textChanged.connect(self.update_new_stroke_color)
        self.undoneStrokeColorInput.textChanged.connect(self.update_undone_stroke_color)
        self.gridColorInput1.textChanged.connect(self.update_grid_color1)
        self.gridColorInput2.textChanged.connect(self.update_grid_color2)
        self.gridDashLenInput1.textChanged.connect(self.update_grid_dash_len1)
        self.gridDashLenInput2.textChanged.connect(self.update_grid_dash_len2)
        self.gridDashSpaceInput1.textChanged.connect(self.update_grid_dash_space1)
        self.gridDashSpaceInput2.textChanged.connect(self.update_grid_dash_space2)
        self.gridWidthInput1.textChanged.connect(self.update_grid_width1)
        self.gridWidthInput2.textChanged.connect(self.update_grid_width2)
        self.gridVisibility1.toggled.connect(self.update_grid_visibility1)
        self.gridVisibility2.toggled.connect(self.update_grid_visibility2)
        self.borderColorInput.textChanged.connect(self.update_border_color)
        self.borderWidthInput.textChanged.connect(self.update_border_width)
        self.borderVisibility.toggled.connect(self.update_border_visibility)

        self.updatePreviewBtn.clicked.connect(self.update_preview_info)
        self.curCharComboBox.currentIndexChanged.connect(self.change_preview_character)
        self.curStrokeComboBox.currentIndexChanged.connect(self.change_preview_stroke)

        self.outputDirSelectBtn.clicked.connect(self.output_dir_select)
        
        self.startBtn.clicked.connect(self.start_process)
        self.closeBtn.clicked.connect(self.close)
        
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))

    def get_cur_character_list(self):
        text = self.inputTextEdit.toPlainText()
        character_list = [char for char in text if "\u4e00" <= char <= "\u9fff"]
        return character_list

    def update_done_stroke_color(self):
        self.config.update({"doneStrokeColor": self.doneStrokeColorInput.text()})

    def update_new_stroke_color(self):
        self.config.update({"newStrokeColor": self.newStrokeColorInput.text()})

    def update_undone_stroke_color(self):
        self.config.update({"undoneStrokeColor": self.undoneStrokeColorInput.text()})

    def update_grid_color1(self):
        self.config.update({"gridColor1": self.gridColorInput1.text()})

    def update_grid_color2(self):
        self.config.update({"gridColor2": self.gridColorInput2.text()})

    def update_grid_dash_len1(self):
        self.config.update({"gridDashLen1": self.gridDashLenInput1.text()})

    def update_grid_dash_len2(self):
        self.config.update({"gridDashLen2": self.gridDashLenInput2.text()})

    def update_grid_dash_space1(self):
        self.config.update({"gridDashSpace1": self.gridDashSpaceInput1.text()})

    def update_grid_dash_space2(self):
        self.config.update({"gridDashSpace2": self.gridDashSpaceInput2.text()})

    def update_grid_width1(self):
        self.config.update({"gridWidth1": self.gridWidthInput1.text()})

    def update_grid_width2(self):
        self.config.update({"gridWidth2": self.gridWidthInput2.text()})

    def update_grid_visibility1(self):
        self.config.update({"gridVisibility1": self.gridVisibility1.isChecked()})

    def update_grid_visibility2(self):
        self.config.update({"gridVisibility2": self.gridVisibility2.isChecked()})

    def update_border_color(self):
        self.config.update({"borderColor": self.borderColorInput.text()})

    def update_border_width(self):
        self.config.update({"borderWidth": self.borderWidthInput.text()})

    def update_border_visibility(self):
        self.config.update({"borderVisibility": self.borderVisibility.isChecked()})
        
    def update_output_dir(self):
        self.config.update({"outputDir": self.outputDirInput.text()})
        
    def output_dir_select(self):
        """选择输出目录"""
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.outputDirInput.setText(dir_path)
            self.config.update({"outputDir": dir_path})

    def change_preview_character(self):
        # 获取当前字符和笔画索引
        curCharacter = self.curCharComboBox.currentText()
        curStrokeIndex = self.curStrokeComboBox.currentText()
        if not curStrokeIndex or not curCharacter:
            return
        character = Character(curCharacter)
        self.curStrokeComboBox.clear()
        self.curStrokeComboBox.addItems(
            [str(i) for i in range(1, character.get_stroke_count() + 2)]
        )
        self.curStrokeComboBox.setCurrentIndex(0)
        self.totalStrokeLabel.setText(str(character.get_stroke_count() + 1))

        # 更新预览
        self.update_preview_render()

    def change_preview_stroke(self):
        # 获取当前字符和笔画索引
        curCharacter = self.curCharComboBox.currentText()
        curStrokeIndex = self.curStrokeComboBox.currentText()
        if not curStrokeIndex or not curCharacter:
            return
        character = Character(curCharacter)
        self.totalStrokeLabel.setText(str(character.get_stroke_count() + 1))

        # 更新预览
        self.update_preview_render()

    def update_preview_info(self):
        # 获取当前字符列表
        character_list = self.get_cur_character_list()
        if not character_list:
            self.curCharComboBox.clear()
            self.curStrokeComboBox.clear()
            self.totalStrokeLabel.setText("0")
            self.previewSvgItem = None
            return

        self.curCharComboBox.clear()
        self.curCharComboBox.addItems(character_list)
        self.curCharComboBox.setCurrentIndex(0)
        self.curStrokeComboBox.clear()
        curCharacter = Character(character_list[0])
        self.curStrokeComboBox.addItems(
            [str(i) for i in range(1, curCharacter.get_stroke_count() + 2)]
        )
        self.curStrokeComboBox.setCurrentIndex(0)
        self.totalStrokeLabel.setText(str(curCharacter.get_stroke_count() + 1))

        # 更新预览
        self.strokePreview.setScene(QtWidgets.QGraphicsScene())
        self.strokePreview.setRenderHint(QtGui.QPainter.Antialiasing)
        self.strokePreview.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.update_preview_render()

    def update_preview_render(self):
        curCharacter = self.curCharComboBox.currentText()
        curStrokeIndex = self.curStrokeComboBox.currentText()
        character = Character(curCharacter)
        svg = get_character_svg_at_index(
            character,
            cur_idx=int(curStrokeIndex) - 1,
            **self.get_render_info(),
        )
        self.previewSvgItem = get_qt_svg_item(svg)
        render_svg_to_view(self.previewSvgItem, self.strokePreview)
        # render_svg_to_view_from_str(svg, self.strokePreview)

        # self.strokePreview.fitInView(svg_item, Qt.KeepAspectRatio)
        
    def start_process(self):
        # 获取当前字符列表
        character_list = self.get_cur_character_list()
        if not character_list:
            return

        # 获取输出目录
        output_dir = self.config.get("outputDir", os.path.join(os.getcwd(), "output"))
        if not output_dir:
            raise ValueError("输出目录未设置，请检查配置。")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 遍历每个字符，生成 SVG 文件
        for char_idx, character in enumerate(character_list):
            # 更新进度条
            self.progressBar.setValue(int((char_idx) / len(character_list) * 100))
            char_obj = Character(character)
            svgs = get_character_svgs_in_range(
                char_obj,
                start_idx=0,
                end_idx=char_obj.get_stroke_count() + 1,
                **self.get_render_info(),
            )
            char_output_dir = os.path.join(output_dir, character)
            os.makedirs(char_output_dir, exist_ok=True)
            for i, svg in enumerate(svgs):
                svg_file_path = os.path.join(char_output_dir, f"{i + 1}.svg")
                with open(svg_file_path, "w", encoding="utf-8") as file:
                    file.write(svg)
            
        # 更新进度条
        self.progressBar.setValue(100)

    def resizeEvent(self, event):
        """主窗口大小变化时调整视图"""
        super().resizeEvent(event)
        self.on_preview_resize()

    def on_preview_resize(self):
        if self.previewSvgItem:
            self.strokePreview.fitInView(
                self.previewSvgItem, Qt.AspectRatioMode.KeepAspectRatio
            )

    def get_render_info(self):
        return {
            "height": 1000,
            "border_color": (
                self.config.get("borderColor", "#000000")
                if self.borderVisibility.isChecked()
                else "#00000000"
            ),
            "border_width": int(self.config.get("borderWidth", "2")),
            "grid_colors": [
                (
                    self.config.get("gridColor1", "#DDDDDD")
                    if self.gridVisibility1.isChecked()
                    else "#00000000"
                ),
                (
                    self.config.get("gridColor1", "#DDDDDD")
                    if self.gridVisibility1.isChecked()
                    else "#00000000"
                ),
                (
                    self.config.get("gridColor2", "#DDDDDD")
                    if self.gridVisibility2.isChecked()
                    else "#00000000"
                ),
                (
                    self.config.get("gridColor2", "#DDDDDD")
                    if self.gridVisibility2.isChecked()
                    else "#00000000"
                ),
            ],
            "grid_dasharray": [
                f"{self.config.get('gridDashLen1', '3')} {self.config.get('gridDashSpace1', '3')}",
                f"{self.config.get('gridDashLen1', '3')} {self.config.get('gridDashSpace1', '3')}",
                f"{self.config.get('gridDashLen2', '3')} {self.config.get('gridDashSpace2', '3')}",
                f"{self.config.get('gridDashLen2', '3')} {self.config.get('gridDashSpace2', '3')}",
            ],
            "grid_width": [
                float(self.config.get("gridWidth1", "0.5")),
                float(self.config.get("gridWidth1", "0.5")),
                float(self.config.get("gridWidth2", "0.5")),
                float(self.config.get("gridWidth2", "0.5")),
            ],
        }

    def load_config(self):
        self.doneStrokeColorInput.setText(self.config.get("doneStrokeColor", "#000000"))
        self.newStrokeColorInput.setText(self.config.get("newStrokeColor", "#FF0000"))
        self.undoneStrokeColorInput.setText(
            self.config.get("undoneStrokeColor", "#555555")
        )
        self.gridColorInput1.setText(self.config.get("gridColor1", "#DDDDDD"))
        self.gridColorInput2.setText(self.config.get("gridColor2", "#DDDDDD"))
        self.gridDashLenInput1.setText(self.config.get("gridDashLen1", "3"))
        self.gridDashLenInput2.setText(self.config.get("gridDashLen2", "3"))
        self.gridDashSpaceInput1.setText(self.config.get("gridDashSpaceInput1", "3"))
        self.gridDashSpaceInput2.setText(self.config.get("gridDashSpaceInput2", "3"))
        self.gridWidthInput1.setText(self.config.get("gridWidth1", "0.5"))
        self.gridWidthInput2.setText(self.config.get("gridWidth2", "0.5"))
        self.gridVisibility1.setChecked(self.config.get("gridVisibility1", True))
        self.gridVisibility2.setChecked(self.config.get("gridVisibility2", True))
        self.borderColorInput.setText(self.config.get("borderColor", "#000000"))
        self.borderWidthInput.setText(self.config.get("borderWidth", "2"))
        self.borderVisibility.setChecked(self.config.get("borderVisibility", True))
        self.outputDirInput.setText(
            self.config.get("outputDir", os.path.join(os.getcwd(), "output"))
        )

        temp_data = {
            "doneStrokeColor": self.doneStrokeColorInput.text(),
            "newStrokeColor": self.newStrokeColorInput.text(),
            "undoneStrokeColor": self.undoneStrokeColorInput.text(),
            "gridColor1": self.gridColorInput1.text(),
            "gridColor2": self.gridColorInput2.text(),
            "gridDashLen1": self.gridDashLenInput1.text(),
            "gridDashLen2": self.gridDashLenInput2.text(),
            "gridDashSpace1": self.gridDashSpaceInput1.text(),
            "gridDashSpace2": self.gridDashSpaceInput2.text(),
            "gridWidth1": self.gridWidthInput1.text(),
            "gridWidth2": self.gridWidthInput2.text(),
            "gridVisibility1": self.gridVisibility1.isChecked(),
            "gridVisibility2": self.gridVisibility2.isChecked(),
            "borderColor": self.borderColorInput.text(),
            "borderWidth": self.borderWidthInput.text(),
            "borderVisibility": self.borderVisibility.isChecked(),
            "outputDir": self.outputDirInput.text(),
        }

        self.config.update(temp_data)
