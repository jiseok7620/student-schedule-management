from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import sqlite3
import traceback

class MyModal(QDialog):
    def __init__(self, parent, nameid, bookname, bookid, datetime, globalSchool, globalGrade, seq):
        try:
            super(MyModal, self).__init__(parent)
            option_ui = 'pyqt_ui/schedule.ui'
            uic.loadUi(option_ui, self)
            self.show()
            self.object = parent

            # 전역변수 선언
            self.seq = seq
            self.stpage = ""
            self.edpage = ""

            # linetext에 이름, 교재, 일자 표시
            self.lineEdit.setText(str(nameid))
            self.lineEdit_2.setText(str(bookname))
            self.lineEdit_3.setText(str(datetime))

            # 테이블 설정
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tableWidget2.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # -- 테이블1에 데이터 표시하기 --
            # 교재 테이블에서 값 가져오기
            cs.execute("SELECT * FROM textbook WHERE bookid =? and startPage <>'-' ORDER BY startPage", (bookid,))
            booklist = cs.fetchall() # 해당 교재의 전체 단원 가져오기

            cs.execute("SELECT * FROM progress WHERE id =? and bookname =? and \
                    strftime('%Y-%m-%d', datetime, 'localtime') <= strftime('%Y-%m-%d', ?, 'localtime') ORDER BY startPage", (nameid, bookid,datetime,))
            progresslist = cs.fetchall() # 해당 학생의 해당 교재 진도율 가져오기

            resultlist = []
            for i in range(0, len(booklist)):
                resultlist.append("-")

            for i in range(0, len(booklist)):
                for j in range(0, len(progresslist)):
                    if booklist[i][5] == progresslist[j][2]:
                        resultlist[i] = progresslist[j][5]
                        break

            self.tableWidget.setRowCount(len(booklist))
            num = 0
            for tbl in booklist:
                self.tableWidget.setItem(num, 0, QTableWidgetItem(str(tbl[2])))
                self.tableWidget.setItem(num, 1, QTableWidgetItem(str(tbl[3])))
                self.tableWidget.setItem(num, 2, QTableWidgetItem(str(tbl[4])))
                self.tableWidget.setItem(num, 3, QTableWidgetItem(str(tbl[5])))
                self.tableWidget.setItem(num, 4, QTableWidgetItem(str(tbl[6])))
                self.tableWidget.setItem(num, 5, QTableWidgetItem(str(resultlist[num])))
                num += 1

            # -- 테이블2에 데이터 표시하기 --
            cs.execute("SELECT * FROM textbook WHERE bookid =? and startPage ='-' ORDER BY startPage", (bookid,))
            booklist2 = cs.fetchall()  # 해당 교재의 전체 단원 가져오기

            self.tableWidget2.setRowCount(len(booklist2))
            num2 = 0
            for tbl2 in booklist2:
                self.tableWidget2.setItem(num2, 0, QTableWidgetItem(str(tbl2[2])))
                self.tableWidget2.setItem(num2, 1, QTableWidgetItem(str(tbl2[3])))
                self.tableWidget2.setItem(num2, 2, QTableWidgetItem(str(tbl2[4])))
                num2 += 1

            # db close
            conn.close()

            # 테이블 더블클릭 시 이벤트
            self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)
            self.tableWidget2.doubleClicked.connect(self.tableWidget2_doubleClicked)

            # 버튼 클릭 시 이벤트
            self.pushButton.clicked.connect(self.enterButtonClick)  # 입력
            self.pushButton2.clicked.connect(self.cancleButtonClick)  # 취소

        except:
            traceback.print_exc()


    def tableWidget_doubleClicked(self):
        row = self.tableWidget.currentIndex().row()
        subject1 = self.tableWidget.item(row, 1).text()
        subject2 = self.tableWidget.item(row, 2).text()
        self.stpage = self.tableWidget.item(row, 3).text()
        self.edpage = self.tableWidget.item(row, 4).text()
        dis_text = subject1 + " [" + subject2 + "] " + "p." + self.stpage + "~" + self.edpage
        self.lineEdit_4.setText(dis_text)

    def tableWidget2_doubleClicked(self):
        row = self.tableWidget2.currentIndex().row()
        subject1 = self.tableWidget2.item(row, 1).text()
        subject2 = self.tableWidget2.item(row, 2).text()

        if subject2 == "단원평가":
            dis_text = subject1 + " <font color=red>단원평가</font>"
        elif subject2 == "오답쓰기":
            dis_text = subject1 + " 오답쓰기(<font color=red>평가준비</font>)"
        elif subject2 == "개념평가":
            dis_text = subject1 + " <font color=red>개념평가</font>"

        self.lineEdit_4.setText(dis_text)

    def enterButtonClick(self):
        self.object.stpageList[self.seq - 1] = self.stpage
        self.object.edpageList[self.seq - 1] = self.edpage
        if self.seq == 1:
            self.object.labelText1.setText(self.lineEdit_4.text())
        elif self.seq == 2:
            self.object.labelText2.setText(self.lineEdit_4.text())
        elif self.seq == 3:
            self.object.labelText3.setText(self.lineEdit_4.text())
        elif self.seq == 4:
            self.object.labelText4.setText(self.lineEdit_4.text())
        elif self.seq == 5:
            self.object.labelText5.setText(self.lineEdit_4.text())
        elif self.seq == 6:
            self.object.labelText6.setText(self.lineEdit_4.text())
        elif self.seq == 7:
            self.object.labelText7.setText(self.lineEdit_4.text())
        elif self.seq == 8:
            self.object.labelText8.setText(self.lineEdit_4.text())
        self.close()

    def cancleButtonClick(self):
        self.close()