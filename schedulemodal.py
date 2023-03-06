from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import sqlite3
import traceback

class MyModal(QDialog):
    def __init__(self, parent, nameid, bookname, bookid, datetime, globalSchool, globalGrade):
        try:
            super(MyModal, self).__init__(parent)
            option_ui = 'pyqt_ui/schedule.ui'
            uic.loadUi(option_ui, self)
            self.show()

            # 전역변수 선언
            self.prepro = ""
            self.aftpro = ""
            self.resultpro = ""

            # linetext에 이름, 교재, 일자 표시
            self.lineEdit.setText(str(nameid))
            self.lineEdit_2.setText(str(bookname))
            self.lineEdit_3.setText(str(datetime))
            
            # -- 테이블에 데이터 표시하기 --
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()
            
            # 교재 테이블에서 값 가져오기
            cs.execute("SELECT * FROM textbook WHERE bookid =?", (bookid,))
            booklist = cs.fetchall() # 해당 교재의 전체 단원 가져오기
            print(booklist)

            cs.execute("SELECT startPage, endPage FROM progress WHERE id =? and bookname =? and \
                    strftime('%Y-%m-%d', datetime, 'localtime') <= strftime('%Y-%m-%d', ?, 'localtime')", (nameid, bookid,datetime,))
            progresslist = cs.fetchall() # 해당 학생의 해당 교재 진도율 가져오기
            print(progresslist)

            for i in range(0, len(booklist)):
                self.prepro = "0"
                self.aftpro = "0"
                for j in range(0,len(progresslist)):
                    if progresslist[j][0] <= booklist[i][5] <= progresslist[j][1]:
                        self.prepro = "1"
                    if progresslist[j][0] <= booklist[i][6] <= progresslist[j][1]:
                        self.aftpro = "1"
                if self.prepro == "1" and self.aftpro == "1":
                    self.resultpro = "완료"
                elif self.prepro == "0" and self.aftpro == "0":
                    self.resultpro = "-"
                else :
                    self.resultpro = "진행중"
                print(booklist[i])
                print(type(booklist[i]))

                booklist[i] = list
                booklist[i].insert(-1, self.resultpro)

            self.tableWidget.setRowCount(len(booklist))
            num = 0
            for tbl in booklist:
                self.tableWidget.setItem(num, 0, QTableWidgetItem(str(tbl[2])))
                self.tableWidget.setItem(num, 1, QTableWidgetItem(str(tbl[3])))
                self.tableWidget.setItem(num, 2, QTableWidgetItem(str(tbl[4])))
                self.tableWidget.setItem(num, 3, QTableWidgetItem(str(tbl[5])))
                self.tableWidget.setItem(num, 4, QTableWidgetItem(str(tbl[6])))
                self.tableWidget.setItem(num, 5, QTableWidgetItem("-"))
                num += 1

            # db close
            conn.close()

        except:
            traceback.print_exc()
