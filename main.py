import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
            self.stuname = "" # 스케줄관리 탭의 학생 이름
            self.globalSchool = ""  # 스케줄관리 탭의 학교
            self.globalGrade = ""  # 스케줄관리 탭의 학년
            self.comboList = [] # 스케줄관리 탭의 교재 리스트
            self.stuId2 = "" # 진도관리 탭의 학생 id
            self.globalSchool2 = "" # 진도관리 탭의 학교
            self.globalGrade2 = "" # 진도관리 탭의 학년
            self.comboList2 = [] # 진도관리 탭의 교재 리스트

            # 전역변수 페이지
            self.stpageList = ["", "", "", "", "", "", "", ""]
            self.edpageList = ["", "", "", "", "", "", "", ""]

            # ---- 시작 시 데이터 베이스 조작 ----
            # 데이터베이스 생성 및 테이블 생성
            conn = sqlite3.connect("inmanage.db", isolation_level=None) # isolation_level=None : 자동커밋
            cs = conn.cursor()  # 커서 획득
            # 테이블이 존재하지 않다면 테이블 만들기
            # 1. 학생테이블
            cs.execute("CREATE TABLE IF NOT EXISTS student \
                    (id integer PRIMARY KEY, name text, sex text, age integer, school text, grade integer, schoolName text, \
                    number text, parentName text, parentSex text, parentNumber text, registDate text)")
            # 2. 교재테이블
            cs.execute("CREATE TABLE IF NOT EXISTS textbook \
                    (bookid text, no text, bookname text, subjectName text, subjectName2 text, startPage text, endPage text, allPage text, \
                    school text, grade text)")
            # 3. 교재할당테이블
            cs.execute("CREATE TABLE IF NOT EXISTS textbookperman \
                    (id integer, book1 text, book2 text, book3 text, book4 text, book5 text, book6 text, book7 text, book8 text, book9 text, book10 text, \
                    CONSTRAINT fk_textbook_group FOREIGN KEY (id) REFERENCES student(id) ON DELETE CASCADE)")
            # 4. 진도테이블
            cs.execute("CREATE TABLE IF NOT EXISTS progress \
                    (id integer, bookname text, startPage text, endPage text, datetime text, remark text, position text, \
                    CONSTRAINT fk_progress_group FOREIGN KEY (id) REFERENCES student(id) ON DELETE CASCADE)")
            # 5. 스케줄테이블
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
            self.btnLeft.clicked.connect(lambda: self.buttonClick("left")) # 스케줄관리 - ◀ 버튼클릭
            self.btnRight.clicked.connect(lambda: self.buttonClick("right")) # 스케줄관리 - ▶ 버튼클릭
            self.btnYesterday.clicked.connect(lambda: self.buttonClick("yesterday"))  # 스케줄관리 - "전날과제 불러오기" 버튼클릭
            self.btnClear.clicked.connect(lambda: self.buttonClick("clear"))  # 스케줄관리 - 초기화 버튼클릭

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
            self.combobook_2.activated.connect(lambda: self.combobookChange(self.combobook_2.currentText(), self.combobook_2.currentIndex(), 2))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_3.activated.connect(lambda: self.combobookChange(self.combobook_3.currentText(), self.combobook_3.currentIndex(), 3))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_4.activated.connect(lambda: self.combobookChange(self.combobook_4.currentText(), self.combobook_4.currentIndex(), 4))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_5.activated.connect(lambda: self.combobookChange(self.combobook_5.currentText(), self.combobook_5.currentIndex(), 5))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_6.activated.connect(lambda: self.combobookChange(self.combobook_6.currentText(), self.combobook_6.currentIndex(), 6))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_7.activated.connect(lambda: self.combobookChange(self.combobook_7.currentText(), self.combobook_7.currentIndex(), 7))  # 스케줄관리 - 교재 리스트 변경시
            self.combobook_8.activated.connect(lambda: self.combobookChange(self.combobook_8.currentText(), self.combobook_8.currentIndex(), 8))  # 스케줄관리 - 교재 리스트 변경시

            # 체크박스 뗄 때 이벤트 처리
            self.checkBox.released.connect(lambda: self.checkboxReleased(1))
            self.checkBox_2.released.connect(lambda: self.checkboxReleased(2))
            self.checkBox_3.released.connect(lambda: self.checkboxReleased(3))
            self.checkBox_4.released.connect(lambda: self.checkboxReleased(4))
            self.checkBox_5.released.connect(lambda: self.checkboxReleased(5))
            self.checkBox_6.released.connect(lambda: self.checkboxReleased(6))
            self.checkBox_7.released.connect(lambda: self.checkboxReleased(7))
            self.checkBox_8.released.connect(lambda: self.checkboxReleased(8))

            # DateEdit 날짜 변경 시 이벤트 처리
            self.dateEdit.dateChanged.connect(self.dateChange)

            # 콤보박스, 리스트위젯 초기화
            self.insertStudentCombo()
            self.comboStudentlistChange()
            self.insertStudent2Combo()
            self.comboStudentlist2Change()

            self.screenShot()
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
                    self.tableWidget.setItem(num, 5, QTableWidgetItem(str(row[6])))
                    self.tableWidget.setItem(num, 6, QTableWidgetItem(str(row[7])))
                    self.tableWidget.setItem(num, 7, QTableWidgetItem(str(row[10])))
                    self.tableWidget.setItem(num, 8, QTableWidgetItem(str(row[11])))
                    self.tableWidget.setItem(num, 9, QTableWidgetItem("-"))
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

            elif what == "yesterday":
                thisdate = self.dateEdit.text().split('-')
                now = dt.datetime(int(thisdate[0]), int(thisdate[1]), int(thisdate[2]))
                before_one_day = now - dt.timedelta(days=1)
                yearVar = before_one_day.year
                monVar = before_one_day.month
                dayVar = before_one_day.day
                montext = str(monVar)
                daytext = str(dayVar)
                if monVar < 10 :
                    montext = "0" + str(monVar)
                if dayVar < 10 :
                    daytext = "0" + str(dayVar)
                dateText = str(yearVar) + "-" + montext + "-" + daytext

                # db connect
                conn = sqlite3.connect("inmanage.db", isolation_level=None)
                cs = conn.cursor()

                # 데이터넣기
                cs.execute("SELECT assign1, assign2, assign3, assign4 FROM schedule WHERE id =? and datetime =?", (self.stuId, dateText,))
                dataList = cs.fetchone()
                for i in range(0, 4):
                    if dataList[i] == "|||False|0":
                        continue

                    assign = dataList[i].split('|')
                    if i == 0:
                        self.combosch1.setCurrentText(assign[0])
                        self.combobook.setCurrentText(assign[1])
                        self.labelText1.setText(assign[2])
                        if assign[3] == "True":
                            self.checkBox.setCheckState(2)  # 2: True, 0: False
                        else :
                            self.checkBox.setCheckState(0)  # 2: True, 0: False
                    if i == 1:
                        self.combosch2.setCurrentText(assign[0])
                        self.combobook_2.setCurrentText(assign[1])
                        self.labelText2.setText(assign[2])
                        if assign[3] == "True":
                            self.checkBox_2.setCheckState(2)  # 2: True, 0: False
                        else :
                            self.checkBox_2.setCheckState(0)  # 2: True, 0: False
                    if i == 2:
                        self.combosch3.setCurrentText(assign[0])
                        self.combobook_3.setCurrentText(assign[1])
                        self.labelText3.setText(assign[2])
                        if assign[3] == "True":
                            self.checkBox_3.setCheckState(2)  # 2: True, 0: False
                        else :
                            self.checkBox_3.setCheckState(0)  # 2: True, 0: False
                    if i == 3:
                        self.combosch4.setCurrentText(assign[0])
                        self.combobook_4.setCurrentText(assign[1])
                        self.labelText4.setText(assign[2])
                        if assign[3] == "True":
                            self.checkBox_4.setCheckState(2)  # 2: True, 0: False
                        else :
                            self.checkBox_4.setCheckState(0)  # 2: True, 0: False

                # 페이지 번호넣기
                cs.execute("SELECT * FROM progress WHERE id =? and datetime =? and position >=5 and position <=8", (self.stuId, dateText,))
                resultList = cs.fetchall()

                for re in resultList:
                    print(re[2], re[3])
                    if re[6] == '5':
                        self.stpageList[0] = re[2]
                        self.edpageList[0] = re[3]
                    elif re[6] == '6':
                        self.stpageList[1] = re[2]
                        self.edpageList[1] = re[3]
                    elif re[6] == '7':
                        self.stpageList[2] = re[2]
                        self.edpageList[2] = re[3]
                    elif re[6] == '8':
                        self.stpageList[3] = re[2]
                        self.edpageList[3] = re[3]
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

                    # schedule 테이블에 데이터 저장하기
                    content1 = self.combosch1.currentText() + "|" + self.combobook.currentText() + "|" + self.labelText1.text() + "|" + str(self.checkBox.isChecked()) + "|" + str(self.combobook.currentIndex())
                    content2 = self.combosch2.currentText() + "|" + self.combobook_2.currentText() + "|" + self.labelText2.text() + "|" + str(self.checkBox_2.isChecked()) + "|" + str(self.combobook_2.currentIndex())
                    content3 = self.combosch3.currentText() + "|" + self.combobook_3.currentText() + "|" + self.labelText3.text() + "|" + str(self.checkBox_3.isChecked()) + "|" + str(self.combobook_3.currentIndex())
                    content4 = self.combosch4.currentText() + "|" + self.combobook_4.currentText() + "|" + self.labelText4.text() + "|" + str(self.checkBox_4.isChecked()) + "|" + str(self.combobook_4.currentIndex())
                    assign1 = self.combosch5.currentText() + "|" + self.combobook_5.currentText() + "|" + self.labelText5.text() + "|" + str(self.checkBox_5.isChecked()) + "|" + str(self.combobook_5.currentIndex())
                    assign2 = self.combosch6.currentText() + "|" + self.combobook_6.currentText() + "|" + self.labelText6.text() + "|" + str(self.checkBox_6.isChecked()) + "|" + str(self.combobook_6.currentIndex())
                    assign3 = self.combosch7.currentText() + "|" + self.combobook_7.currentText() + "|" + self.labelText7.text() + "|" + str(self.checkBox_7.isChecked()) + "|" + str(self.combobook_7.currentIndex())
                    assign4 = self.combosch8.currentText() + "|" + self.combobook_8.currentText() + "|" + self.labelText8.text() + "|" + str(self.checkBox_8.isChecked()) + "|" + str(self.combobook_8.currentIndex())
                    notice1 = self.lineEditNotice1.text()
                    notice2 = self.lineEditNotice2.text()
                    if content1 == "|||False|0" and content2 == "|||False|0" and content3 == "|||False|0" and content4 == "|||False|0" and assign1 == "|||False|0" and assign2 == "|||False|0" and assign3 == "|||False|0" and assign4 == "|||False|0":
                        pass
                    else :
                        insert_list = (
                            (stid, stdatetime, content1, content2, content3, content4, assign1, assign2, assign3, assign4, notice1, notice2)
                        )
                        cs.execute("INSERT INTO schedule(id, datetime, content1, content2, content3, content4, assign1, assign2, assign3, assign4, notice1, notice2) \
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", insert_list)
                    
                    # progress 테이블에 데이터 저장하기
                    contentlist1 = content1.split('|')
                    contentlist2 = content2.split('|')
                    contentlist3 = content3.split('|')
                    contentlist4 = content4.split('|')
                    assignlist1 = assign1.split('|')
                    assignlist2 = assign2.split('|')
                    assignlist3 = assign3.split('|')
                    assignlist4 = assign4.split('|')
                    emptyBoolList = [contentlist1[4], contentlist2[4], contentlist3[4], contentlist4[4], assignlist1[4], assignlist2[4], assignlist3[4], assignlist4[4]]
                    checkBoxBoolList = [contentlist1[3], contentlist2[3], contentlist3[3], contentlist4[3], assignlist1[3], assignlist2[3], assignlist3[3], assignlist4[3]]
                    # 해당 일자의 데이터는 일단 모두 제거
                    cs.execute("DELETE FROM progress WHERE id =? and datetime =?", (stid, stdatetime, ))
                    for i in range(0, 8):
                        if emptyBoolList[i] == "0":
                            continue
                        else :
                            if checkBoxBoolList[i] == "True":
                                insert_list2 = ((stid, self.comboList[int(emptyBoolList[i])-1], self.stpageList[i], self.edpageList[i], stdatetime, "진행중", str(i+1)))
                            else :
                                insert_list2 = ((stid, self.comboList[int(emptyBoolList[i])-1], self.stpageList[i], self.edpageList[i], stdatetime, "완료", str(i+1)))
                        # 시작페이지가 없다면 저장하지않는다.
                        if self.stpageList[i] == "":
                            continue
                        # 시작페이지가 있다면 저장한다.
                        else :
                            cs.execute("SELECT COUNT(*) FROM progress WHERE id =? and bookname =? and startPage =? and strftime('%Y-%m-%d', datetime, 'localtime') <= strftime('%Y-%m-%d', ?, 'localtime')", (stid, self.comboList[int(emptyBoolList[i])-1], self.stpageList[i], stdatetime,))
                            result = cs.fetchone()
                            print(result)
                            # 과거에 해당 시작페이지가 progress에 존재하지않다면 추가하기
                            if result[0] == 0:
                                cs.execute("INSERT INTO progress(id, bookname, startPage, endPage, datetime, remark, position) VALUES(?,?,?,?,?,?,?)", insert_list2)
                            # 과거에 해당 시작페이지가 progress에 존재한다면 과거데이터는 제거하고 추가하기
                            else:
                                cs.execute("DELETE FROM progress WHERE id =? and startPage =? and strftime('%Y-%m-%d', datetime, 'localtime') <= strftime('%Y-%m-%d', ?, 'localtime')", (stid, self.stpageList[i], stdatetime,))
                                cs.execute("INSERT INTO progress(id, bookname, startPage, endPage, datetime, remark, position) VALUES(?,?,?,?,?,?,?)", insert_list2)
                    
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

    def checkboxReleased(self, seq):
        try :
            if seq == 1:
                if self.checkBox.isChecked():
                    enterText = self.labelText1.text() + " (<font color=red>진행중</font>)"
                    self.labelText1.setText(enterText)
                else:
                    enterText = self.labelText1.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText1.setText(enterText)
            if seq == 2:
                if self.checkBox_2.isChecked():
                    enterText = self.labelText2.text() + " (<font color=red>진행중</font>)"
                    self.labelText2.setText(enterText)
                else:
                    enterText = self.labelText2.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText2.setText(enterText)
            if seq == 3:
                if self.checkBox_3.isChecked():
                    enterText = self.labelText3.text() + " (<font color=red>진행중</font>)"
                    self.labelText3.setText(enterText)
                else:
                    enterText = self.labelText3.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText3.setText(enterText)
            if seq == 4:
                if self.checkBox_4.isChecked():
                    enterText = self.labelText4.text() + " (<font color=red>진행중</font>)"
                    self.labelText4.setText(enterText)
                else:
                    enterText = self.labelText4.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText4.setText(enterText)
            if seq == 5:
                if self.checkBox_5.isChecked():
                    enterText = self.labelText5.text() + " (<font color=red>진행중</font>)"
                    self.labelText5.setText(enterText)
                else:
                    enterText = self.labelText5.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText5.setText(enterText)
            if seq == 6:
                if self.checkBox_6.isChecked():
                    enterText = self.labelText6.text() + " (<font color=red>진행중</font>)"
                    self.labelText6.setText(enterText)
                else:
                    enterText = self.labelText6.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText6.setText(enterText)
            if seq == 7:
                if self.checkBox_7.isChecked():
                    enterText = self.labelText7.text() + " (<font color=red>진행중</font>)"
                    self.labelText7.setText(enterText)
                else:
                    enterText = self.labelText7.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText7.setText(enterText)
            if seq == 8:
                if self.checkBox_8.isChecked():
                    enterText = self.labelText8.text() + " (<font color=red>진행중</font>)"
                    self.labelText8.setText(enterText)
                else:
                    enterText = self.labelText8.text().strip(" (<font color=red>진행중</font>)")
                    self.labelText8.setText(enterText)
        except:
            traceback.print_exc()

    # ------------------------------------------------------------------------
    # 스케줄관리 탭
    def screenShot(self):
        dateText = self.dateEdit.text()
        filepath = ""
        filename = self.globalSchool + "_" + self.globalGrade + "_" + self.stuname + "_" + dateText
        stX = 160
        stY = 45
        width = 800 - stX
        height = 600 - stY
        grab = self.grab(QRect(stX,stY,width,height))
        grab.save(filename + '.png', 'png')

        '''
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId(), 0, 0, 100 , 100)
        screenshot.save(filename + '.jpg', 'jpg')
        '''

    def dateChange(self):
        self.searchScheData()

    def scheduleClear(self):
        # 날짜 : 월-일[요일] 형식으로 넣기
        # thisdate = schedulelist[1].split('-')
        thisdate = self.dateEdit.text().split('-')
        now = dt.datetime(int(thisdate[0]), int(thisdate[1]), int(thisdate[2]))
        yearVar = now.year
        monVar = now.month
        dayVar = now.day
        days = ['월', '화', '수', '목', '금', '토', '일']
        daysVar = days[dt.date(yearVar, monVar, dayVar).weekday()]
        self.labelDate.setText(str(monVar) + "/" + str(dayVar) + "[" + daysVar + "]")
        
        # 나머지는 초기화
        self.combosch1.setCurrentText("")
        self.combobook.setCurrentText("")
        self.labelText1.setText("")
        self.checkBox.setCheckState(0)  # 2: True, 0: False
        self.combosch2.setCurrentText("")
        self.combobook_2.setCurrentText("")
        self.labelText2.setText("")
        self.checkBox_2.setCheckState(0)  # 2: True, 0: False
        self.combosch3.setCurrentText("")
        self.combobook_3.setCurrentText("")
        self.labelText3.setText("")
        self.checkBox_3.setCheckState(0)  # 2: True, 0: False
        self.combosch4.setCurrentText("")
        self.combobook_4.setCurrentText("")
        self.labelText4.setText("")
        self.checkBox_4.setCheckState(0)  # 2: True, 0: False
        self.combosch5.setCurrentText("")
        self.combobook_5.setCurrentText("")
        self.labelText5.setText("")
        self.checkBox_5.setCheckState(0)  # 2: True, 0: False
        self.combosch6.setCurrentText("")
        self.combobook_6.setCurrentText("")
        self.labelText6.setText("")
        self.checkBox_6.setCheckState(0)  # 2: True, 0: False
        self.combosch7.setCurrentText("")
        self.combobook_7.setCurrentText("")
        self.labelText7.setText("")
        self.checkBox_7.setCheckState(0)  # 2: True, 0: False
        self.combosch8.setCurrentText("")
        self.combobook_8.setCurrentText("")
        self.labelText8.setText("")
        self.checkBox_8.setCheckState(0)  # 2: True, 0: False
        self.lineEditNotice1.setText("")
        self.lineEditNotice2.setText("")

        # 시작, 끝 페이지 초기화
        self.stpageList = ["", "", "", "", "", "", "", ""]
        self.edpageList = ["", "", "", "", "", "", "", ""]

    def searchScheData(self):
        try :
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # 교재 테이블에서 값 가져오기
            cs.execute("SELECT * FROM schedule WHERE id =? and datetime =?", (self.stuId, self.dateEdit.text(), ))
            schedulelist = cs.fetchone()  # 해당 교재의 전체 단원 가져오기
            if schedulelist == None :
                # 알림창
                reply = QMessageBox.about(self, "알림창!!", "해당 일자의 스케줄데이터가 존재하지않습니다.")
                # 스케줄 초기화
                self.scheduleClear()
                return
            else :
                # 값 채워넣기
                # 날짜 : 월-일[요일] 형식으로 넣기
                #thisdate = schedulelist[1].split('-')
                thisdate = self.dateEdit.text().split('-')
                now = dt.datetime(int(thisdate[0]), int(thisdate[1]), int(thisdate[2]))
                yearVar = now.year
                monVar = now.month
                dayVar = now.day
                days = ['월', '화', '수', '목', '금', '토', '일']
                daysVar = days[dt.date(yearVar, monVar, dayVar).weekday()]
                self.labelDate.setText(str(monVar) + "/" + str(dayVar) + "[" + daysVar + "]")

                # 나머지 값들
                content1 = schedulelist[2].split('|')
                self.combosch1.setCurrentText(str(content1[0]))
                self.combobook.setCurrentText(str(content1[1]))
                self.labelText1.setText(str(content1[2]))
                if content1[3] == "True":
                    self.checkBox.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox.setCheckState(0)
                content2 = schedulelist[3].split('|')
                self.combosch2.setCurrentText(str(content2[0]))
                self.combobook_2.setCurrentText(str(content2[1]))
                self.labelText2.setText(str(content2[2]))
                if content2[3] == "True":
                    self.checkBox_2.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_2.setCheckState(0)
                content3 = schedulelist[4].split('|')
                self.combosch3.setCurrentText(str(content3[0]))
                self.combobook_3.setCurrentText(str(content3[1]))
                self.labelText3.setText(str(content3[2]))
                if content3[3] == "True":
                    self.checkBox_3.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_3.setCheckState(0)
                content4 = schedulelist[5].split('|')
                self.combosch4.setCurrentText(str(content4[0]))
                self.combobook_4.setCurrentText(str(content4[1]))
                self.labelText4.setText(str(content4[2]))
                if content4[3] == "True":
                    self.checkBox_4.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_4.setCheckState(0)
                assign1 = schedulelist[6].split('|')
                self.combosch5.setCurrentText(str(assign1[0]))
                self.combobook_5.setCurrentText(str(assign1[1]))
                self.labelText5.setText(str(assign1[2]))
                if assign1[3] == "True":
                    self.checkBox_5.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_5.setCheckState(0)
                assign2 = schedulelist[7].split('|')
                self.combosch6.setCurrentText(str(assign2[0]))
                self.combobook_6.setCurrentText(str(assign2[1]))
                self.labelText6.setText(str(assign2[2]))
                if assign2[3] == "True":
                    self.checkBox_6.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_6.setCheckState(0)
                assign3 = schedulelist[8].split('|')
                self.combosch7.setCurrentText(str(assign3[0]))
                self.combobook_7.setCurrentText(str(assign3[1]))
                self.labelText7.setText(str(assign3[2]))
                if assign3[3] == "True":
                    self.checkBox_7.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_7.setCheckState(0)
                assign4 = schedulelist[9].split('|')
                self.combosch8.setCurrentText(str(assign4[0]))
                self.combobook_8.setCurrentText(str(assign4[1]))
                self.labelText8.setText(str(assign4[2]))
                if assign4[3] == "True":
                    self.checkBox_8.setCheckState(2) # 2: True, 0: False
                else :
                    self.checkBox_8.setCheckState(0)
                self.lineEditNotice1.setText(str(schedulelist[10]))
                self.lineEditNotice2.setText(str(schedulelist[11]))
                
                # 진도 데이터를 읽어서 stpageList, edpageList 바꾸기
                self.stpageList = ["", "", "", "", "", "", "", ""]
                self.edpageList = ["", "", "", "", "", "", "", ""]
                cs.execute("SELECT * FROM progress WHERE id =? and datetime =?", (self.stuId, self.dateEdit.text(),))
                progressList = cs.fetchall()
                pgnum = 0
                for pg in progressList:
                    if pg[6] == "1":
                        self.stpageList[0] = pg[2]
                        self.edpageList[0] = pg[3]
                    elif pg[6] == "2":
                        self.stpageList[1] = pg[2]
                        self.edpageList[1] = pg[3]
                    elif pg[6] == "3":
                        self.stpageList[2] = pg[2]
                        self.edpageList[2] = pg[3]
                    elif pg[6] == "4":
                        self.stpageList[3] = pg[2]
                        self.edpageList[3] = pg[3]
                    elif pg[6] == "5":
                        self.stpageList[4] = pg[2]
                        self.edpageList[4] = pg[3]
                    elif pg[6] == "6":
                        self.stpageList[5] = pg[2]
                        self.edpageList[5] = pg[3]
                    elif pg[6] == "7":
                        self.stpageList[6] = pg[2]
                        self.edpageList[6] = pg[3]
                    elif pg[6] == "8":
                        self.stpageList[7] = pg[2]
                        self.edpageList[7] = pg[3]
                    pgnum += 1

                print(self.stpageList)
                print(self.edpageList)
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
                    self.combosch1.setCurrentText("")
                    self.stpageList[0] = ""
                    self.edpageList[0] = ""
                    self.checkBox.setCheckState(0)  # 2: True, 0: False
                elif seq == 2:
                    self.labelText2.setText("")
                    self.combosch2.setCurrentText("")
                    self.stpageList[1] = ""
                    self.edpageList[1] = ""
                    self.checkBox_2.setCheckState(0)  # 2: True, 0: False
                elif seq == 3:
                    self.labelText3.setText("")
                    self.combosch3.setCurrentText("")
                    self.stpageList[2] = ""
                    self.edpageList[2] = ""
                    self.checkBox_3.setCheckState(0)  # 2: True, 0: False
                elif seq == 4:
                    self.labelText4.setText("")
                    self.combosch4.setCurrentText("")
                    self.stpageList[3] = ""
                    self.edpageList[3] = ""
                    self.checkBox_4.setCheckState(0)  # 2: True, 0: False
                elif seq == 5:
                    self.labelText5.setText("")
                    self.combosch5.setCurrentText("")
                    self.stpageList[4] = ""
                    self.edpageList[4] = ""
                    self.checkBox_5.setCheckState(0)  # 2: True, 0: False
                elif seq == 6:
                    self.labelText6.setText("")
                    self.combosch6.setCurrentText("")
                    self.stpageList[5] = ""
                    self.edpageList[5] = ""
                    self.checkBox_6.setCheckState(0)  # 2: True, 0: False
                elif seq == 7:
                    self.labelText7.setText("")
                    self.combosch7.setCurrentText("")
                    self.stpageList[6] = ""
                    self.edpageList[6] = ""
                    self.checkBox_7.setCheckState(0)  # 2: True, 0: False
                elif seq == 8:
                    self.labelText8.setText("")
                    self.combosch8.setCurrentText("")
                    self.stpageList[7] = ""
                    self.edpageList[7] = ""
                    self.checkBox_8.setCheckState(0)  # 2: True, 0: False
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
            self.stuname = self.listWidget.currentItem().text() # 클릭한 list의 값 = 학생이름
            cs.execute("SELECT id FROM student WHERE name =? and school =? and grade =?",
                       (self.stuname, self.globalSchool, self.globalGrade,))
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
            self.labelName.setText(self.stuname)

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
            if stutext == "":
                return
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
            if stutext == "":
                return
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
            cs.execute("SELECT * FROM progress WHERE id =? and bookname =? ORDER BY startPage",
                       (self.stuId2, self.comboSchool.currentText(),))
            acceptList = cs.fetchall()
            self.tableWidget2.setRowCount(len(acceptList))
            num = 0
            for row in acceptList:
                self.tableWidget2.setItem(num, 0, QTableWidgetItem(str(row[1])))
                self.tableWidget2.setItem(num, 1, QTableWidgetItem(str(row[2])))
                self.tableWidget2.setItem(num, 2, QTableWidgetItem(str(row[3])))
                self.tableWidget2.setItem(num, 3, QTableWidgetItem(str(row[4])))
                self.tableWidget2.setItem(num, 4, QTableWidgetItem(str(row[5])))
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
            progressRate = sum / int(pageAll) * 100
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