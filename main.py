import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import assignmodal
import enrollmodal
import bookmodal
import buttonobject
import traceback
import layout
import datetime
import schedulemodal

form_class = uic.loadUiType("pyqt_ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)

            # 현재시간 입력하기
            to_day = datetime.datetime.now()
            yearVar = to_day.year
            monVar = to_day.month
            dayVar = to_day.day
            dateVar = QDate(yearVar, monVar, dayVar)
            self.dateEdit.setDate(dateVar)
            self.dateEdit2.setDate(dateVar)

            # 레이아웃 설정
            layout.MainLayout(self)
            days = ['월','화','수','목','금','토','일']
            daysVar = days[datetime.date(yearVar, monVar, dayVar).weekday()]
            self.labelDate.setText(self.dateEdit.text()+"["+daysVar+"]")

            # 전역변수 선언
            self.mainId = "0" # 메인 id
            self.mainName = "" # 메인 이름
            self.stuId = ""  # 스케줄관리 탭의 학생 id
            self.globalSchool = ""  # 스케줄관리 탭의 학교
            self.globalGrade = ""  # 스케줄관리 탭의 학년
            self.comboList = [] # 스케줄관리 탭의 교재 리스트
            self.stuId2 = "" # 진도관리 탭의 학생 id
            self.globalSchool2 = "" # 진도관리 탭의 학교
            self.globalGrade2 = "" # 진도관리 탭의 학년
            self.comboList2 = [] # 진도관리 탭의 교재 리스트

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
                    (bookid text, no integer, bookname text, subjectName text, subjectName2 text, startPage integer, endPage integer, allPage integer, \
                    school text, grade text)")
            # 3. 교재할당테이블
            cs.execute("CREATE TABLE IF NOT EXISTS textbookperman \
                    (id integer, book1 text, book2 text, book3 text, book4 text, book5 text, book6 text, book7 text, book8 text, book9 text, book10 text, \
                    CONSTRAINT fk_textbook_group FOREIGN KEY (id) REFERENCES student(id) ON DELETE CASCADE)")
            # 4. 진도테이블
            cs.execute("CREATE TABLE IF NOT EXISTS progress \
                    (id integer, bookname text, startPage integer, endPage integer, datetime text, \
                    CONSTRAINT fk_progress_group FOREIGN KEY (id) REFERENCES student(id) ON DELETE CASCADE)")

            conn.close() # db close

            # 테이블 설정
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tableWidget2.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            # 테이블 클릭시
            self.tableWidget.cellClicked.connect(self.tableCellClicked) # 테이블 셀 클릭시

            # 버튼 클릭
            self.btnEnroll.clicked.connect(lambda: self.buttonClick("enroll")) # 인원등록
            self.btnDelete.clicked.connect(lambda: self.buttonClick("delete")) # 인원삭제
            self.btnUpdate.clicked.connect(lambda: self.buttonClick("update")) # 인원수정
            self.btnSearch.clicked.connect(lambda: self.buttonClick("search")) # 인원검색
            self.btnScSearch.clicked.connect(lambda: self.buttonClick("scsearch"))  # 스케줄관리 - 검색 버튼클릭
            self.btnLeft.clicked.connect(lambda: self.buttonClick("left")) # 스케줄관리 - ◀ 버튼클릭
            self.btnRight.clicked.connect(lambda: self.buttonClick("right")) # 스케줄관리 - ▶ 버튼클릭
            self.btnProDelete.clicked.connect(lambda: self.buttonClick("prodelete"))  # 진도관리 - 삭제 버튼클릭
            self.btnProAdd.clicked.connect(lambda: self.buttonClick("proadd"))  # 진도관리 - 추가 버튼클릭

            # 메뉴 클릭
            self.action_book.triggered.connect(lambda: self.menuClick("book")) # 교재등록
            self.action_assign.triggered.connect(lambda: self.menuClick("assign"))  # 교재할당

            # 리스트위젯 아이템 클릭시 이벤트 처리
            self.listWidget.itemClicked.connect(self.listWidgetClick)
            self.listWidget2.itemClicked.connect(self.listWidget2Click)

            # 콤보박스 변경 시 이벤트 처리
            self.comboStudentList.currentTextChanged.connect(self.comboStudentlistChange)  # 스케줄관리 - 학년 리스트 변경시
            self.comboStudentList2.currentTextChanged.connect(self.comboStudentlist2Change)  # 진도관리 - 한년 리스트 변경시
            self.comboSchool.currentTextChanged.connect(self.comboSchoolChange)  #  진도관리 - 교재명 리스트 변경시
            self.combobook.activated.connect(lambda: self.combobookChange(self.combobook.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_2.activated.connect(lambda: self.combobookChange(self.combobook_2.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_3.activated.connect(lambda: self.combobookChange(self.combobook_3.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_4.activated.connect(lambda: self.combobookChange(self.combobook_4.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_5.activated.connect(lambda: self.combobookChange(self.combobook_5.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_6.activated.connect(lambda: self.combobookChange(self.combobook_6.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_7.activated.connect(lambda: self.combobookChange(self.combobook_7.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_8.activated.connect(lambda: self.combobookChange(self.combobook_8.currentText(), self.combobook.currentIndex()))  # 스케줄관리 - 교재 리스트 변경시

            # 콤보박스, 리스트위젯 초기화
            self.insertStudentCombo()
            self.comboStudentlistChange()
            self.insertStudent2Combo()
            self.comboStudentlist2Change()
        except:
            traceback.print_exc()

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

            elif what == "scsearch":
                pass

            elif what == "left":
                pass

            elif what == "right":
                pass

            elif what == "prodelete":
                buttonobject.MyApp.btnprodeleteClick()

            elif what == "proadd":
                stid = self.stuId2
                bookname = self.comboSchool.currentText()
                startpage = self.bookTitle.text()
                endpage = self.lineEdit.text()
                datetime = self.dateEdit2.text()
                acceptList = buttonobject.MyApp.btnproaddClick(self, stid, bookname, startpage, endpage, datetime)
                self.tableWidget2.setRowCount(len(acceptList))
                num = 0
                for row in acceptList:
                    self.tableWidget2.setItem(num, 0, QTableWidgetItem(str(row[1])))
                    self.tableWidget2.setItem(num, 1, QTableWidgetItem(str(row[2])))
                    self.tableWidget2.setItem(num, 2, QTableWidgetItem(str(row[3])))
                    self.tableWidget2.setItem(num, 3, QTableWidgetItem(str(row[4])))
                    num += 1

        except:
            traceback.print_exc()



    def menuClick(self, what):
        if what == "book":
            modal = bookmodal.MyModal(self) # 모달 띄우기
        elif what == "assign":
            modal = assignmodal.MyModal(self) # 모달 띄우기



    def tableCellClicked(self, row, col):
        self.mainId = self.tableWidget.item(row, 0).text()
        self.mainName = self.tableWidget.item(row, 1).text()

    # ------------------------------------------------------------------------
    # 스케줄관리 탭
    def combobookChange(self, bookname, index):
        try:
            if index-1 == -1:
                return
            else:
                # self.comboList[index-1] : bookid
                modal = schedulemodal.MyModal(self, self.stuId, bookname, self.comboList[index-1], self.dateEdit.text(), self.globalSchool, self.globalGrade)
        except:
            traceback.print_exc()

    def listWidgetClick(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 콤보박스 초기화
            self.combobook.clear()
            self.combobook_2.clear()
            self.combobook_3.clear()
            self.combobook_4.clear()
            self.combobook_5.clear()
            self.combobook_6.clear()
            self.combobook_7.clear()
            self.combobook_8.clear()
            self.combobook.addItem("")
            self.combobook_2.addItem("")
            self.combobook_3.addItem("")
            self.combobook_4.addItem("")
            self.combobook_5.addItem("")
            self.combobook_6.addItem("")
            self.combobook_7.addItem("")
            self.combobook_8.addItem("")

            # 해당 인원의 ID 찾기
            stuname = self.listWidget.currentItem().text() # 클릭한 list의 값 = 학생이름
            cs.execute("SELECT id FROM student WHERE name =? and school =? and grade =?",
                       (stuname, self.globalSchool, self.globalGrade,))
            namelist = cs.fetchone()
            self.stuId = namelist[0]
            if namelist == None:
                reply = QMessageBox.about(self, "알림창!", "해당 학생은 존재하지 않습니다.")
                return

            # 할당 교재 리스트 넣기
            cs.execute("SELECT * FROM textbookperman WHERE id =?", (namelist[0],))
            booklist = cs.fetchone()
            self.comboList = [] # 학생 교재리스트 전역변수에 값넣기
            if booklist == None :
                reply = QMessageBox.about(self, "알림창!", "해당 학생은 할당된 교재가 존재하지 않습니다.")
                return
            for i in range(1, len(booklist)):
                if str(booklist[i]) == "":
                    break
                self.comboList.append(booklist[i])
                cs.execute("SELECT bookname FROM textbook WHERE bookid =?", (booklist[i],))
                resultname = cs.fetchone()
                self.combobook.addItem(resultname[0])
                self.combobook_2.addItem(resultname[0])
                self.combobook_3.addItem(resultname[0])
                self.combobook_4.addItem(resultname[0])
                self.combobook_5.addItem(resultname[0])
                self.combobook_6.addItem(resultname[0])
                self.combobook_7.addItem(resultname[0])
                self.combobook_8.addItem(resultname[0])

            # db close
            conn.close()

            # 양식에 이름 넣기
            self.labelName.setText(stuname)

        except:
            traceback.print_exc()
            # db close
            conn.close()


    def insertStudentCombo(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 콤보박스 초기화
            self.comboStudentList.clear()

            # 교재 리스트 콤보박스에 값 넣기
            cs.execute("SELECT DISTINCT school || '-' || grade FROM student")
            bookk = cs.fetchall()
            sortlist = []
            for bk in bookk:
                sortlist.append(bk[0])
            sortlist.sort(reverse=True)
            for sl in sortlist:
                self.comboStudentList.addItem(sl)

            # db close
            conn.close()

        except:
            traceback.print_exc()
            # db close
            conn.close()


    def comboStudentlistChange(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 리스트위젯 초기화
            self.listWidget.clear()

            # 리스트위젯에 값넣기
            stutext = self.comboStudentList.currentText()
            self.globalSchool = stutext.split('-')[0]
            self.globalGrade = stutext.split('-')[1]
            cs.execute("SELECT name FROM student WHERE school =? and grade =?",
                       (self.globalSchool, self.globalGrade,))
            stulist = cs.fetchall()
            sortlist = []
            for sl in stulist:
                sortlist.append(sl[0])
            sortlist.sort()
            for sl in sortlist:
                self.listWidget.addItem(sl)

            # db close
            conn.close()
        except:
            traceback.print_exc()
            # db close
            conn.close()


    # ------------------------------------------------------------------------
    # 진도관리 탭
    def listWidget2Click(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 콤보박스 초기화
            self.comboSchool.clear()

            # 해당 인원의 ID 찾기
            stuname = self.listWidget2.currentItem().text() # 클릭한 list의 값 = 학생이름
            cs.execute("SELECT id FROM student WHERE name =? and school =? and grade =?",
                       (stuname, self.globalSchool2, self.globalGrade2,))
            namelist = cs.fetchone()
            self.stuId2 = namelist[0]
            if namelist == None:
                reply = QMessageBox.about(self, "알림창!", "해당 학생은 존재하지 않습니다.")
                return

            # 할당 교재 리스트 넣기
            cs.execute("SELECT * FROM textbookperman WHERE id =?", (namelist[0],))
            booklist = cs.fetchone()
            if booklist == None :
                reply = QMessageBox.about(self, "알림창!", "해당 학생은 할당된 교재가 존재하지 않습니다.")
                return
            for i in range(1, len(booklist)):
                if str(booklist[i]) == "":
                    break
                self.comboSchool.addItem(booklist[i])

            # db close
            conn.close()

            # 학생 교재리스트 전역변수에 값넣기
            combonum = self.comboSchool.count()
            self.comboList2 = []
            for i in range(0, combonum):
                self.comboList2.append(self.comboSchool.itemText(i))

            # 진도율 넣기
            self.displayProgressBar()

        except:
            traceback.print_exc()
            # db close
            conn.close()

    def insertStudent2Combo(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 콤보박스 초기화
            self.comboStudentList2.clear()

            # 교재 리스트 콤보박스에 값 넣기
            cs.execute("SELECT DISTINCT school || '-' || grade FROM student")
            bookk = cs.fetchall()
            sortlist = []
            for bk in bookk:
                sortlist.append(bk[0])
            sortlist.sort(reverse=True)
            for sl in sortlist:
                self.comboStudentList2.addItem(sl)

            # db close
            conn.close()

        except:
            traceback.print_exc()
            # db close
            conn.close()


    def comboStudentlist2Change(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()
            
            # 리스트위젯 초기화
            self.listWidget2.clear()
            
            # 리스트위젯에 값넣기
            stutext = self.comboStudentList2.currentText()
            self.globalSchool2 = stutext.split('-')[0]
            self.globalGrade2 = stutext.split('-')[1]
            cs.execute("SELECT name FROM student WHERE school =? and grade =?", (self.globalSchool2, self.globalGrade2,))
            stulist = cs.fetchall()
            sortlist = []
            for sl in stulist:
                sortlist.append(sl[0])
            sortlist.sort()
            for sl in sortlist:
                self.listWidget2.addItem(sl)

            # db close
            conn.close()
        except:
            traceback.print_exc()
            # db close
            conn.close()


    def comboSchoolChange(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 진도관리탭 테이블 초기화
            self.tableWidget2.setRowCount(0)

            # 테이블에 데이터 넣기
            cs.execute("SELECT * FROM progress WHERE id =? and bookname =?",
                       (self.stuId2, self.comboSchool.currentText(),))
            acceptList = cs.fetchall()
            self.tableWidget2.setRowCount(len(acceptList))
            num = 0
            for row in acceptList:
                self.tableWidget2.setItem(num, 0, QTableWidgetItem(str(row[1])))
                self.tableWidget2.setItem(num, 1, QTableWidgetItem(str(row[2])))
                self.tableWidget2.setItem(num, 2, QTableWidgetItem(str(row[3])))
                self.tableWidget2.setItem(num, 3, QTableWidgetItem(str(row[4])))
                num += 1

            # db close
            conn.close()

            # 진도율 넣기
            self.displayProgressBar()

        except:
            traceback.print_exc()
            # db close
            conn.close()


    def displayProgressBar(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # ProgressBar 초기화하기
            self.progressBar.reset()

            # 해당 인원의 사용교재 가져오기 = self.comboList2
            # 사용교재별 진도율 구하기
            # 진행페이지 수의 총합 / 총 페이지 수 * 100
            bookname = self.comboSchool.currentText()
            cs.execute("SELECT allPage FROM textbook WHERE bookid =?", (bookname,))
            pagelist = cs.fetchone()
            if pagelist == None :
                return
            pageAll = pagelist[0]

            cs.execute("SELECT endPage - startPage FROM progress WHERE id =? and bookname =?", (self.stuId2, bookname,))
            pageSepar = cs.fetchall()
            sum = 0
            for ps in pageSepar:
                sum += ps[0] + 1

            # ProgressBar에 표시하기
            progressRate = sum / pageAll * 100
            self.progressBar.setValue(int(progressRate))

            # db close
            conn.close()

        except:
            traceback.print_exc()
            # db close
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()