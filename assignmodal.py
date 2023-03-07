from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import sqlite3
import traceback

class MyModal(QDialog):
    def __init__(self, parent):
        try:
            super(MyModal, self).__init__(parent)
            option_ui = 'pyqt_ui/assign.ui'
            uic.loadUi(option_ui, self)
            self.show()

            # 전역변수 선언
            self.globalSchool = ""
            self.globalGrade = ""
            self.tableRowNum = ""

            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()
            
            # 이름리스트 넣기
            cs.execute("SELECT name FROM student WHERE school =? and grade =?", (self.comboSchool.currentText(), self.comboGrade.currentText(),))
            namelist = cs.fetchall()
            for nl in namelist:
                self.comboName.addItem(nl[0])

            # db close
            conn.close()
            
            # 버튼 클릭 이벤트 처리
            self.btndelete.clicked.connect(lambda: self.btnDelete())  # 삭제
            self.btnsave.clicked.connect(lambda: self.btnSave())  # 저장

            # 콤보박스 변경 시 이벤트 처리
            self.comboBooklist.currentTextChanged.connect(self.comboBooklistChange) # 교재 리스트 변경시
            self.comboSchool.currentTextChanged.connect(self.comboSchoollistChange) # 학교 리스트 변경시
            self.comboGrade.currentTextChanged.connect(self.comboGradelistChange) # 학년 리스트 변경시
            self.comboName.currentTextChanged.connect(self.comboNamelistChange) # 이름 변경시

            # 리스트위젯-테이블 드래그 앤 드롭
            self.tableWidget = QTableWidgetDrop(self)
            self.listWidget = drop_list(self)
            self.verticalLayout_3.addWidget(self.listWidget)
            self.verticalLayout_2.addWidget(self.tableWidget)

            # 테이블 설정
            self.tableWidget.setColumnCount(2)
            column_headers = ['학생ID', '교재ID']
            self.tableWidget.setHorizontalHeaderLabels(column_headers)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            # 테이블 클릭시
            self.tableWidget.cellClicked.connect(self.tableCellClicked)  # 테이블 셀 클릭시

            # 교재 리스트 콤보박스에 값 넣기
            self.insertCombo()

            # 모든 교재를 조회하여 listWidget에 표시하기
            self.comboBooklistChange()

            # 해당 이름의 id를 넣기
            self.comboNamelistChange()

        except:
            traceback.print_exc()

    def tableCellClicked(self, row, col):
        self.tableRowNum = row

    def comboSchoollistChange(self):
        # db connect
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        # 콤보박스 초기화
        self.comboName.clear()

        # 테이블 초기화
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        column_headers = ['학생ID', '교재ID']

        # 이름리스트 넣기
        cs.execute("SELECT name FROM student WHERE school =? and grade =?",
                   (self.comboSchool.currentText(), self.comboGrade.currentText(),))
        namelist = cs.fetchall()
        for nl in namelist:
            self.comboName.addItem(nl[0])

        # db close
        conn.close()

    def comboGradelistChange(self):
        # db connect
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        # 콤보박스 초기화
        self.comboName.clear()

        # 테이블 초기화
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        column_headers = ['학생ID', '교재ID']

        # 이름리스트 넣기
        cs.execute("SELECT name FROM student WHERE school =? and grade =?",
                   (self.comboSchool.currentText(), self.comboGrade.currentText(),))
        namelist = cs.fetchall()
        for nl in namelist:
            self.comboName.addItem(nl[0])

        # db close
        conn.close()

    def comboNamelistChange(self):
        # db connect
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        # 텍스트박스 초기화
        self.textStudentId.clear()

        # 테이블 초기화
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        column_headers = ['학생ID', '교재ID']

        # 이름리스트 넣기
        cs.execute("SELECT id FROM student WHERE name =? and school =? and grade =?", (self.comboName.currentText(), self.comboSchool.currentText(), self.comboGrade.currentText(),))
        namelist = cs.fetchone()
        if namelist == None :
            pass
        else :
            self.textStudentId.setText(str(namelist[0]))
        
        # 리스트 보여주기
        self.bookTableView()
        
        # db close
        conn.close()

    def bookTableView(self):
        # db connect
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        # 이름리스트 넣기
        cs.execute("SELECT * FROM textbookperman WHERE id =?", (self.textStudentId.text(),))
        booklist = cs.fetchone()
        if booklist == None :
            pass
        else:
            for i in range(1,len(booklist)):
                if str(booklist[i]) == "" :
                    break
                self.tableWidget.insertRow(i-1)
                self.tableWidget.setItem(i-1, 0, QTableWidgetItem(str(booklist[0])))
                self.tableWidget.setItem(i-1, 1, QTableWidgetItem(str(booklist[i])))

        # db close
        conn.close()



    def btnDelete(self):
        try:
            # 삭제 메세지
            reply = QMessageBox.question(self, '경고창!!', str(self.tableRowNum) + '번 행을 지우시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 테이블 행 삭제
                self.tableWidget.removeRow(int(self.tableRowNum))
            else:
                pass
        except:
            traceback.print_exc()



    def btnSave(self):
        try:
            if self.tableWidget.rowCount() == 0:
                # db connect
                conn = sqlite3.connect("inmanage.db", isolation_level=None)
                cs = conn.cursor()

                # 해당 교재의 모든항목을 삭제
                cs.execute("DELETE FROM textbookperman WHERE id =?", (self.textStudentId.text(),))

                # 완료메세지
                reply = QMessageBox.about(self, "Success!!", "저장이 완료되었습니다.")
            else:
                # db connect
                conn = sqlite3.connect("inmanage.db", isolation_level=None)
                cs = conn.cursor()

                # 해당 교재의 모든항목을 삭제
                cs.execute("DELETE FROM textbookperman WHERE id =?", (self.textStudentId.text(),))

                # 다시 테이블에 입력된 모든값을 저장
                book1, book2, book3, book4, book5, book6, book7, book8, book9, book10 = "", "", "", "", "", "", "", "", "", ""
                for i in range(0, self.tableWidget.rowCount()):
                    stid = self.tableWidget.item(i, 0).text()
                    if i == 0:
                        book1 = self.tableWidget.item(i, 1).text()
                    elif i == 1:
                        book2 = self.tableWidget.item(i, 1).text()
                    elif i == 2:
                        book3 = self.tableWidget.item(i, 1).text()
                    elif i == 3:
                        book4 = self.tableWidget.item(i, 1).text()
                    elif i == 4:
                        book5 = self.tableWidget.item(i, 1).text()
                    elif i == 5:
                        book6 = self.tableWidget.item(i, 1).text()
                    elif i == 6:
                        book7 = self.tableWidget.item(i, 1).text()
                    elif i == 7:
                        book8 = self.tableWidget.item(i, 1).text()
                    elif i == 8:
                        book9 = self.tableWidget.item(i, 1).text()
                    elif i == 9:
                        book10 = self.tableWidget.item(i, 1).text()

                insert_list = (
                    (stid, book1, book2, book3, book4, book5, book6, book7, book8, book9, book10)
                )
                cs.execute("INSERT INTO textbookperman(id, book1, book2, book3, book4, book5, book6, book7, book8, book9, book10) \
                                                VALUES(?,?,?,?,?,?,?,?,?,?,?)", insert_list)

                # db close
                conn.close()

                # 완료메세지
                reply = QMessageBox.about(self, "Success!!", "저장이 완료되었습니다.")

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
            for sl in sortlist:
                self.comboBooklist.addItem(sl)

            # db close
            conn.close()

        except:
            traceback.print_exc()



    def comboBooklistChange(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            self.listWidget.clear()
            bootext = self.comboBooklist.currentText()
            if bootext == "":
                return
            self.globalSchool = bootext.split('-')[0]
            self.globalGrade = bootext.split('-')[1]
            cs.execute("SELECT DISTINCT bookname FROM textbook WHERE school =? and grade =?", (self.globalSchool, self.globalGrade,))
            booklist = cs.fetchall()
            for bl in booklist:
                self.listWidget.addItem(bl[0])

            # db close
            conn.close()

        except:
            traceback.print_exc()

            # db close
            conn.close()



    def dragAndDrop(self, bookname):
        if self.textStudentId.text() == "" or self.comboName.currentText() == "" :
            reply = QMessageBox.about(self, "알림창!", "학생을 먼저 선택해주세요.")
            return
        else :
            pass
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 해당 교재의 ID 가져오기
            cs.execute("SELECT DISTINCT bookid FROM textbook WHERE bookname =? and school =? and grade =?", (bookname, self.globalSchool, self.globalGrade,))
            bookid = cs.fetchone()

            # db close
            conn.close()

            # 학생ID와 교재ID를 테이블에 넣기
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(self.textStudentId.text())))
            self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(bookid[0])))



class QTableWidgetDrop(QTableWidget):
    def __init__(self, parent):
        super(QTableWidgetDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.object = parent

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        try:
            MyModal.dragAndDrop(self.object, e.source().currentItem().text())
        except:
            traceback.print_exc()

class drop_list(QListWidget):
    def __init__(self, parent):
        super(drop_list, self).__init__(parent)
        self.setDragEnabled(True)