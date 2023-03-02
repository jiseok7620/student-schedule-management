from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3
import traceback

class MyModal(QDialog):
    def __init__(self, parent):
        try:
            super(MyModal, self).__init__(parent)
            option_ui = 'pyqt_ui/book.ui'
            uic.loadUi(option_ui, self)
            self.show()

            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 교재 리스트 콤보박스에 값 넣기
            self.insertCombo()

            # 모든 교재를 조회하여 listWidget에 표시하기
            self.comboBooklistChange()

            # db close
            conn.close()

            # 테이블 설정
            self.tableWidget.setColumnCount(5)
            column_headers = ['NO', '대단원명', '부단원명', '시작페이지', '끝페이지']
            self.tableWidget.setHorizontalHeaderLabels(column_headers)
            self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            # 버튼 클릭 이벤트 처리
            self.btndelete.clicked.connect(lambda: self.btnDelete())  # 교재삭제
            self.btnsave.clicked.connect(lambda: self.btnSave())  # 교재저장
            self.btndelrow.clicked.connect(lambda: self.btnDelRow())  # 행삭제
            self.btnaddrow.clicked.connect(lambda: self.btnAddRow())  # 행추가

            # 콤보박스 변경 시 이벤트 처리
            self.comboBooklist.currentTextChanged.connect(self.comboBooklistChange)

            # 리스트위젯 아이템 클릭시 이벤트 처리
            self.listWidget.itemClicked.connect(self.listWidgetClick)

        except:
            traceback.print_exc()

    def insertCombo(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 콤보박스 초기화
            self.comboBooklist.clear()

            # 교재 리스트 콤보박스에 값 넣기
            cs.execute("SELECT DISTINCT school || '-' || grade FROM textbook")
            bookk = cs.fetchall()
            sortlist = []
            for bk in bookk:
                sortlist.append(bk[0])
            sortlist.sort(reverse=True)
            for sl in sortlist :
                self.comboBooklist.addItem(sl)

            # db close
            conn.close()

        except:
            traceback.print_exc()



    def btnDelete(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()
            
            # 삭제 메세지
            reply = QMessageBox.question(self, '경고창!!', '정말로 ' + self.bookTitle.text() + '을 지우시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 테이블 삭제
                cs.execute("DELETE FROM textbook WHERE bookname =? and school =? and grade =?",
                           (self.bookTitle.text(), self.comboSchool.currentText(), self.comboGrade.currentText()))

                # 콤보박스 변경
                self.insertCombo()

                # 테이블 초기화
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(5)
                column_headers = ['NO', '대단원명', '부단원명', '시작페이지', '끝페이지']

                # lineedit 초기화
                self.comboSchool.setCurrentText("초등학교")
                self.comboGrade.setCurrentText("1")
                self.bookTitle.setText("")
                self.allPage.setText("")

                # db close
                conn.close()
            else:
                pass
        except:
            traceback.print_exc()



    def btnSave(self):
        try:
            if self.tableWidget.rowCount() == 0:
                reply = QMessageBox.about(self, "알림창!", "테이블에 내용이 없습니다. 내용을 입력해주세요.")
            else :
                # db connect
                conn = sqlite3.connect("inmanage.db", isolation_level=None)
                cs = conn.cursor()

                # 해당 교재의 모든항목을 삭제
                cs.execute("DELETE FROM textbook WHERE bookname =? and school =? and grade =?", (self.bookTitle.text(), self.comboSchool.currentText(), self.comboGrade.currentText()))

                # 다시 테이블에 입력된 모든값을 저장
                for i in range(0, self.tableWidget.rowCount()) :
                    no = self.tableWidget.item(i,0).text()
                    bookname = self.bookTitle.text()
                    subjectname = self.tableWidget.item(i,1).text()
                    subjectname2 = self.tableWidget.item(i,2).text()
                    startpage = self.tableWidget.item(i,3).text()
                    endpage = self.tableWidget.item(i,4).text()
                    allpage = self.allPage.text()
                    school = self.comboSchool.currentText()
                    grade = self.comboGrade.currentText()
                    insert_list = (
                        (no, bookname, subjectname, subjectname2, startpage, endpage, allpage, school, grade)
                    )
                    cs.execute("INSERT INTO textbook(no, bookname, subjectName, subjectName2, startPage, endPage, allPage, school, grade) \
                                                    VALUES(?,?,?,?,?,?,?,?,?)", insert_list)

                # db close
                conn.close()

                # 완료메세지
                reply = QMessageBox.about(self, "Success!!", "저장이 완료되었습니다.")

                # 교재 리스트 콤보박스에 값 넣기
                self.insertCombo()

                # 테이블 초기화
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(5)
                column_headers = ['NO', '대단원명', '부단원명', '시작페이지', '끝페이지']

                # lineedit 초기화
                self.comboSchool.setCurrentText("초등학교")
                self.comboGrade.setCurrentText("1")
                self.bookTitle.setText("")
                self.allPage.setText("")

        except:
            traceback.print_exc()



    def btnDelRow(self):
        rowCount = self.tableWidget.rowCount() - 1
        self.tableWidget.removeRow(rowCount)



    def btnAddRow(self):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(rowCount+1)))



    def comboBooklistChange(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            self.listWidget.clear()
            bootext = self.comboBooklist.currentText()
            sc = bootext.split('-')[0]
            gr = bootext.split('-')[1]
            cs.execute("SELECT DISTINCT bookname FROM textbook WHERE school =? and grade =?", (sc, gr,))
            booklist = cs.fetchall()
            for bl in booklist:
                self.listWidget.addItem(bl[0])

            # db close
            conn.close()

        except:
            traceback.print_exc()

            # db close
            conn.close()



    def listWidgetClick(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 데이터 조회
            booknm = self.listWidget.currentItem().text()
            bootext = self.comboBooklist.currentText()
            sc = bootext.split('-')[0]
            gr = bootext.split('-')[1]
            cs.execute("SELECT * FROM textbook WHERE bookname =? and school =? and grade =?", (booknm, sc, gr,))
            textbooklist = cs.fetchall()
            self.bookTitle.setText(str(textbooklist[0][1]))
            self.allPage.setText(str(textbooklist[0][6]))
            self.comboSchool.setCurrentText(str(textbooklist[0][7]))
            self.comboGrade.setCurrentText(str(textbooklist[0][8]))
            self.tableWidget.setRowCount(len(textbooklist))
            num = 0
            for tbl in textbooklist:
                self.tableWidget.setItem(num, 0, QTableWidgetItem(str(tbl[0])))
                self.tableWidget.setItem(num, 1, QTableWidgetItem(str(tbl[2])))
                self.tableWidget.setItem(num, 2, QTableWidgetItem(str(tbl[3])))
                self.tableWidget.setItem(num, 3, QTableWidgetItem(str(tbl[4])))
                self.tableWidget.setItem(num, 4, QTableWidgetItem(str(tbl[5])))
                num += 1

            # db close
            conn.close()

        except:
            traceback.print_exc()

            # db close
            conn.close()