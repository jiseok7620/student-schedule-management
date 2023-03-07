from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainLayout():
    def __init__(self, parent):
        self.object = parent

        # 1. 아이엔 이미지 넣기
        self.object.pixmap = QPixmap('image/inmainimage.jpg')
        self.object.labelImage.setPixmap(
            self.object.pixmap.scaled(self.object.labelImage.width(), self.object.labelImage.height(), Qt.IgnoreAspectRatio))
        self.object.labelImage.setAlignment(Qt.AlignCenter)

        # 2. 라벨
        self.object.labelDate.setStyleSheet("color: black;"
                                     "border-color: #BFBFBF;"
                                     "background-color: #92CDDD;"
                                     "font: 12pt")
        self.object.labelDaily.setStyleSheet("color: black;"
                                      "border-color: #BFBFBF;"
                                      "background-color: #92CDDD;"
                                      "font: bold 20pt")
        self.object.labelName.setStyleSheet("color: black;"
                                     "border-color: #BFBFBF;"
                                     "background-color: #92CDDD;"
                                     "font: bold 20pt")
        self.object.labelTitle1.setStyleSheet("color: white;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: #BFBFBF;"
                                       "background-color: #8CB3E4;"
                                       "padding: 6px;"
                                       "font: bold 15pt")
        self.object.labelTitle2.setStyleSheet("color: white;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: #BFBFBF;"
                                       "background-color: #C3D69B;"
                                       "padding: 6px;"
                                       "font: bold 15pt")
        self.object.labelTitle3.setStyleSheet("color: white;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: #BFBFBF;"
                                       "background-color: #D99694;"
                                       "padding: 6px;"
                                       "font: bold 15pt")
        self.object.checkBox.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_2.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_3.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_4.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_5.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_6.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_7.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_8.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_9.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.checkBox_10.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "border-bottom-width: 1px;"
                        "border-bottom-color: #BFBFBF;"
                        "border-bottom-style: solid;"
                        "padding-left: 10px;"
                        "padding-right: 10px;"
                        "background-color: white")
        self.object.labelText1.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText2.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText3.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText4.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText5.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText6.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText7.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")
        self.object.labelText8.setStyleSheet(
                        "border-left-width: 1px;"
                        "border-left-color: #BFBFBF;"
                        "border-left-style: solid;"
                        "border-right-width: 1px;"
                        "border-right-color: #BFBFBF;"
                        "border-right-style: solid;"
                        "border-top-width: 1px;"
                        "border-top-color: #BFBFBF;"
                        "border-top-style: solid;"
                        "background-color: white")

        # 3. 콤보박스
        self.object.combosch1.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combosch2.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch3.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch4.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch5.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch6.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch7.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combosch8.setStyleSheet("QComboBox"
                                     "{"
                                     "border-left-width: 1px;"
                                     "border-left-color: #BFBFBF;"
                                     "border-left-style: solid;"
                                     "border-top-width: 1px;"
                                     "border-top-color: #BFBFBF;"
                                     "border-top-style: solid;"
                                     "background: white;"
                                     "font: bold 10pt"
                                     "}"
                                     "QComboBox::drop-down"
                                     "{"
                                     "border: 0px;"
                                     "background-color: white;"
                                     "padding: 0px;"
                                     "}")
        self.object.combobook.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_2.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_3.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_4.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_5.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_6.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_7.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.combobook_8.setStyleSheet("QComboBox"
                                            "{"
                                            "border-left-width: 1px;"
                                            "border-left-color: #BFBFBF;"
                                            "border-left-style: solid;"
                                            "border-top-width: 1px;"
                                            "border-top-color: #BFBFBF;"
                                            "border-top-style: solid;"
                                            "background: white;"
                                            "font: bold 10pt"
                                            "}"
                                            "QComboBox::drop-down"
                                            "{"
                                            "border: 0px;"
                                            "background-color: white;"
                                            "padding: 0px;"
                                            "}")
        self.object.lineEditNotice1.setStyleSheet("color: blue;"
                                         "border-style: solid;"
                                         "border-width: 1px;"
                                         "border-color: #BFBFBF;"
                                         "background-color: white;"
                                         "font: bold 12pt")
        self.object.lineEditNotice2.setStyleSheet("color: blue;"
                                          "border-style: solid;"
                                          "border-width: 1px;"
                                          "border-color: #BFBFBF;"
                                          "background-color: white;"
                                          "font: bold 12pt")