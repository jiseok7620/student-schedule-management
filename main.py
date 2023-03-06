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
import datetime as dt
import schedulemodal

form_class = uic.loadUiType("pyqt_ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)

            # 윈도우 크기고정
            self.setFixedSize(QSize(800, 600))

            # 현재시간 입력하기
            to_day = dt.datetime.now()
            yearVar = to_day.year
            monVar = to_day.month
            dayVar = to_day.day
            dateVar = QDate(yearVar, monVar, dayVar)
            self.dateEdit.setDate(dateVar)
            self.dateEdit2.setDate(dateVar)

            # 레이아웃 설정
            layout.MainLayout(self)
            days = ['월','화','수','목','금','토','일']
            daysVar = days[dt.date(yearVar, monVar, dayVar).weekday()]
            self.labelDate.setText(str(monVar)+"/"+str(dayVar)+"["+daysVar+"]")

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
            # 4. 스케줄테이블
            cs.execute("CREATE TABLE IF NOT EXISTS schedule \
                    (id integer, datetime text, content1 text, content2 text, content3 text, content4 text, \
                    assign1 text, assign2 text, assign3 text, assign4 text, notice1 text, notice2 text, \
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
            self.btnClear.clicked.connect(lambda: self.buttonClick("clear"))  # 스케줄관리 - 초기화 버튼클릭
            self.btnLeft.clicked.connect(lambda: self.buttonClick("left")) # 스케줄관리 - ◀ 버튼클릭
            self.btnRight.clicked.connect(lambda: self.buttonClick("right")) # 스케줄관리 - ▶ 버튼클릭
            self.btnProDelete.clicked.connect(lambda: self.buttonClick("prodelete"))  # 진도관리 - 삭제 버튼클릭
            self.btnProAdd.clicked.connect(lambda: self.buttonClick("proadd"))  # 진도관리 - 추가 버튼클릭

            # 메뉴 클릭
            self.action_book.triggered.connect(lambda: self.menuClick("book")) # 교재등록
            self.action_assign.triggered.connect(lambda: self.menuClick("assign"))  # 교재할당
            self.action_save.triggered.connect(lambda: self.menuClick("save")) # 내보내기

            # 리스트위젯 아이템 클릭시 이벤트 처리
            self.listWidget.itemClicked.connect(self.listWidgetClick)
            self.listWidget2.itemClicked.connect(self.listWidget2Click)

            # 콤보박스 변경 시 이벤트 처리
            self.comboStudentList.currentTextChanged.connect(self.comboStudentlistChange)  # 스케줄관리 - 학년 리스트 변경시
            self.comboStudentList2.currentTextChanged.connect(self.comboStudentlist2Change)  # 진도관리 - 한년 리스트 변경시
            self.comboSchool.currentTextChanged.connect(self.comboSchoolChange)  #  진도관리 - 교재명 리스트 변경시
            self.combobook.activated.connect(lambda: self.combobookChange(self.combobook.currentText(), self.combobook.currentIndex(), 1))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_2.activated.connect(lambda: self.combobookChange(self.combobook_2.currentText(), self.combobook.currentIndex(), 2))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_3.activated.connect(lambda: self.combobookChange(self.combobook_3.currentText(), self.combobook.currentIndex(), 3))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_4.activated.connect(lambda: self.combobookChange(self.combobook_4.currentText(), self.combobook.currentIndex(), 4))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_5.activated.connect(lambda: self.combobookChange(self.combobook_5.currentText(), self.combobook.currentIndex(), 5))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_6.activated.connect(lambda: self.combobookChange(self.combobook_6.currentText(), self.combobook.currentIndex(), 6))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_7.activated.connect(lambda: self.combobookChange(self.combobook_7.currentText(), self.combobook.currentIndex(), 7))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_8.activated.connect(lambda: self.combobookChange(self.combobook_8.currentText(), self.combobook.currentIndex(), 8))  # 스케줄관리 - 교재 리스트 변경시

            # DateEdit 날짜 변경 시 이벤트 처리
            self.dateEdit.dateChanged.connect(self.dateChange)

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
            elif what == "clear":
                self.scheduleClear()

            elif what == "left":
                # 현재시간 입력하기
                thisdate = self.dateEdit.text().split('-')
                now = dt.datetime(int(thisdate[0]), int(thisdate[1]), int(thisdate[2]))
                before_one_day = now - dt.timedelta(days=1)
                yearVar = before_one_day.year
                monVar = before_one_day.month
                dayVar = before_one_day.day
                dateVar = QDate(yearVar, monVar, dayVar)
                self.dateEdit.setDate(dateVar)

            elif what == "right":
                # 현재시간 입력하기
                thisdate = self.dateEdit.text().split('-')
                now = dt.datetime(int(thisdate[0]), int(thisdate[1]), int(thisdate[2]))
                after_one_day = now + dt.timedelta(days=1)
                yearVar = after_one_day.year
                monVar = after_one_day.month
                dayVar = after_one_day.day
                dateVar = QDate(yearVar, monVar, dayVar)
                self.dateEdit.setDate(dateVar)

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
        try:
            if what == "book":
                modal = bookmodal.MyModal(self) # 모달 띄우기
            elif what == "assign":
                modal = assignmodal.MyModal(self) # 모달 띄우기
            elif what == "save":
                # db connect
                conn = sqlite3.connect("inmanage.db", isolation_level=None)
                cs = conn.cursor()

                reply = QMessageBox.question(self, '알림창!!', '저장하시겠습니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 해당 교재의 모든항목을 삭제
                    stid = self.stuId
                    stdatetime = self.dateEdit.text()
                    cs.execute("DELETE FROM schedule WHERE id =? and datetime =?", (stid, stdatetime, ))

                    # 데이터 저장하기
                    content1 = self.combosch1.currentText() + "|" + self.combobook.currentText() + "|" + self.labelText1.text()
                    content2 = self.combosch2.currentText() + "|" + self.combobook_2.currentText() + "|" + self.labelText2.text()
                    content3 = self.combosch3.currentText() + "|" + self.combobook_3.currentText() + "|" + self.labelText3.text()
                    content4 = self.combosch4.currentText() + "|" + self.combobook_4.currentText() + "|" + self.labelText4.text()
                    assign1 = self.combosch5.currentText() + "|" + self.combobook_5.currentText() + "|" + self.labelText5.text()
                    assign2 = self.combosch6.currentText() + "|" + self.combobook_6.currentText() + "|" + self.labelText6.text()
                    assign3 = self.combosch7.currentText() + "|" + self.combobook_7.currentText() + "|" + self.labelText7.text()
                    assign4 = self.combosch8.currentText() + "|" + self.combobook_8.currentText() + "|" + self.labelText8.text()
                    notice1 = self.lineEditNotice1.text()
                    notice2 = self.lineEditNotice2.text()
                    insert_list = (
                        (stid, stdatetime, content1, content2, content3, content4, assign1, assign2, assign3, assign4, notice1, notice2)
                    )
                    cs.execute("INSERT INTO schedule(id, datetime, content1, content2, content3, content4, assign1, assign2, assign3, assign4, notice1, notice2) \
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", insert_list)
                    # db close
                    conn.close()

                else:
                    # db close
                    conn.close()
                    return

                # 이미지로 저장하기
                # 해당일자폴더만들기 => 학교_학년_이름_일자.png 만들기

        except:
            traceback.print_exc()

            # db close
            conn.close()

    def tableCellClicked(self, row, col):
        self.mainId = self.tableWidget.item(row, 0).text()
        self.mainName = self.tableWidget.item(row, 1).text()

    # ------------------------------------------------------------------------
    # 스케줄관리 탭
    def dateChange(self):
        self.searchScheData()

    def scheduleClear(self):
        self.labelDate.setText(str(self.dateEdit.text()))
        self.combosch1.setCurrentText("")
        self.combobook.setCurrentText("")
        self.labelText1.setText("")
        self.combosch2.setCurrentText("")
        self.combobook_2.setCurrentText("")
        self.labelText2.setText("")
        self.combosch3.setCurrentText("")
        self.combobook_3.setCurrentText("")
        self.labelText3.setText("")
        self.combosch4.setCurrentText("")
        self.combobook_4.setCurrentText("")
        self.labelText4.setText("")
        self.combosch5.setCurrentText("")
        self.combobook_5.setCurrentText("")
        self.labelText5.setText("")
        self.combosch6.setCurrentText("")
        self.combobook_6.setCurrentText("")
        self.labelText6.setText("")
        self.combosch7.setCurrentText("")
        self.combobook_7.setCurrentText("")
        self.labelText7.setText("")
        self.combosch8.setCurrentText("")
        self.combobook_8.setCurrentText("")
        self.labelText8.setText("")
        self.lineEditNotice1.setText("")
        self.lineEditNotice2.setText("")

    def searchScheData(self):
        try :
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 교재 테이블에서 값 가져오기
            cs.execute("SELECT * FROM schedule WHERE id =? and datetime =?", (self.stuId, self.dateEdit.text(), ))
            schedulelist = cs.fetchone()  # 해당 교재의 전체 단원 가져오기
            if schedulelist == None :
                reply = QMessageBox.about(self, "알림창!!", "해당 일자의 스케줄데이터가 존재하지않습니다.")
                self.scheduleClear()
                return
            else :
                # 값 채워넣기
                self.labelDate.setText(str(schedulelist[1]))
                content1 = schedulelist[2].split('|')
                self.combosch1.setCurrentText(str(content1[0]))
                self.combobook.setCurrentText(str(content1[1]))
                self.labelText1.setText(str(content1[2]))
                content2 = schedulelist[3].split('|')
                self.combosch2.setCurrentText(str(content2[0]))
                self.combobook_2.setCurrentText(str(content2[1]))
                self.labelText2.setText(str(content2[2]))
                content3 = schedulelist[4].split('|')
                self.combosch3.setCurrentText(str(content3[0]))
                self.combobook_3.setCurrentText(str(content3[1]))
                self.labelText3.setText(str(content3[2]))
                content4 = schedulelist[5].split('|')
                self.combosch4.setCurrentText(str(content4[0]))
                self.combobook_4.setCurrentText(str(content4[1]))
                self.labelText4.setText(str(content4[2]))
                assign1 = schedulelist[6].split('|')
                self.combosch5.setCurrentText(str(assign1[0]))
                self.combobook_5.setCurrentText(str(assign1[1]))
                self.labelText5.setText(str(assign1[2]))
                assign2 = schedulelist[7].split('|')
                self.combosch6.setCurrentText(str(assign2[0]))
                self.combobook_6.setCurrentText(str(assign2[1]))
                self.labelText6.setText(str(assign2[2]))
                assign3 = schedulelist[8].split('|')
                self.combosch7.setCurrentText(str(assign3[0]))
                self.combobook_7.setCurrentText(str(assign3[1]))
                self.labelText7.setText(str(assign3[2]))
                assign4 = schedulelist[9].split('|')
                self.combosch8.setCurrentText(str(assign4[0]))
                self.combobook_8.setCurrentText(str(assign4[1]))
                self.labelText8.setText(str(assign4[2]))
                self.lineEditNotice1.setText(str(schedulelist[10]))
                self.lineEditNotice2.setText(str(schedulelist[11]))

                # db close
                conn.close()
        except:
            traceback.print_exc()

            # db close
            conn.close()

    def combobookChange(self, bookname, index, seq):
        try:
            if index-1 == -1:
                if seq == 1:
                    self.labelText1.setText("")
                elif seq == 2:
                    self.labelText2.setText("")
                elif seq == 3:
                    self.labelText3.setText("")
                elif seq == 4:
                    self.labelText4.setText("")
                elif seq == 5:
                    self.labelText5.setText("")
                elif seq == 6:
                    self.labelText6.setText("")
                elif seq == 7:
                    self.labelText7.setText("")
                elif seq == 8:
                    self.labelText8.setText("")
            else:
                # self.comboList[index-1] : bookid
                modal = schedulemodal.MyModal(self, self.stuId, bookname, self.comboList[index-1], self.dateEdit.text(), self.globalSchool, self.globalGrade, seq)
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

            # 조회하기
            self.searchScheData()

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