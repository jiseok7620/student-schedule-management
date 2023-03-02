import sys
import os
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic
import enrollmodal
import bookmodal
import buttonobject
import traceback


form_class = uic.loadUiType("pyqt_ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 전역변수 선언
        self.mainId = "0" # 메인 id
        self.mainName = "" # 메인 이름

        # ---- 시작 시 데이터 베이스 조작 ----
        # 데이터베이스 생성 및 테이블 생성
        conn = sqlite3.connect("inmanage.db", isolation_level=None) # isolation_level=None : 자동커밋
        cs = conn.cursor()  # 커서 획득
        # 테이블이 존재하지 않다면 테이블 만들기
        # 1. 학생테이블
        cs.execute("CREATE TABLE IF NOT EXISTS student \
                (id integer PRIMARY KEY, name text, sex text, age integer, school text, grade integer, address1 text, \
                address2 text, email text, number text, parentName text, parentSex text, parentNumber text, registDate text)")
        # 2. 교재테이블
        cs.execute("CREATE TABLE IF NOT EXISTS textbook \
                (no integer, bookname text, subjectName text, subjectName2 text, startPage integer, endPage integer, allPage integer, \
                school text, grade text)")

        conn.close() # db close

        # 테이블 설정
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 테이블 클릭시
        self.tableWidget.cellClicked.connect(self.tableCellClicked) # 테이블 셀 클릭시

        # 버튼 클릭
        self.btnEnroll.clicked.connect(lambda: self.buttonClick("enroll")) # 인원등록
        self.btnDelete.clicked.connect(lambda: self.buttonClick("delete")) # 인원삭제
        self.btnUpdate.clicked.connect(lambda: self.buttonClick("update")) # 인원수정
        self.btnSearch.clicked.connect(lambda: self.buttonClick("search")) # 인원검색

        # 메뉴 클릭
        self.action_book.triggered.connect(lambda: self.menuClick("book")) # 교재등록



    def buttonClick(self, what):
        try:
            if what == "enroll":
                modal = enrollmodal.MyModal(self, "enroll", self.mainId) # 등록 모달 띄우기

            elif what == "delete":
                if self.mainId == "0":
                    reply = QMessageBox.about(self, "알림창", "삭제할 셀을 선택해주세요.")
                else :
                    buttonobject.MyApp.btndeleteClick(self, self.mainId, self.mainName)
                    self.mainId = "0"  #메인 id
                    self.mainName = ""  #메인 이름

            elif what == "update":
                if self.mainId == "0" :
                    reply = QMessageBox.about(self, "알림창", "변경할 셀을 선택해주세요.")
                else :
                    modal = enrollmodal.MyModal(self, "update", self.mainId) # 등록 모달 띄우기
                    self.mainId = "0"  #메인 id
                    self.mainName = ""  #메인 이름

            elif what == "search":
                conSchool = self.comboBox.currentText()
                conGrade = self.comboBox_2.currentText()
                returnList = buttonobject.MyApp.btnsearchClick(self, conSchool, conGrade)
                self.tableWidget.setRowCount(len(returnList))
                num = 0
                for row in returnList:
                    self.tableWidget.setItem(num, 0, QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(num, 1, QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(num, 2, QTableWidgetItem(str(row[2])))
                    self.tableWidget.setItem(num, 3, QTableWidgetItem(str(row[4])))
                    self.tableWidget.setItem(num, 4, QTableWidgetItem(str(row[5])))
                    self.tableWidget.setItem(num, 5, QTableWidgetItem(str(row[13])))
                    num += 1
        except:
            traceback.print_exc()




    def menuClick(self, what):
        if what == "book":
            modal = bookmodal.MyModal(self) # 등록 모달 띄우기
        elif what == "save":
            pass
        elif what == "capture":
            pass
        elif what == "pdf":
            pass




    def databaseOper(self, what):
        if what == "db":
            pass
        elif what == "insert":
            pass
        elif what == "select":
            pass




    def radioClicked(self, what):
        if what == "elem":
            pass
        elif what == "midd":
            pass
        elif what == "high":
            pass




    def tableCellClicked(self, row, col):
        self.mainId = self.tableWidget.item(row, 0).text()
        self.mainName = self.tableWidget.item(row, 1).text()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()