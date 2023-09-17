from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3
import traceback

class MyModal(QDialog):
    def __init__(self, parent, what, mainId):
        super(MyModal, self).__init__(parent)
        option_ui = 'pyqt_ui/enroll.ui'
        uic.loadUi(option_ui, self)
        self.show()

        # db connect
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        # 글자 수 제한하기
        # 전화번호
        self.textPhone1.setMaxLength(3)
        self.textPhone2.setMaxLength(4)
        self.textPhone3.setMaxLength(4)
        self.textParentNumber1.setMaxLength(3)
        self.textParentNumber2.setMaxLength(4)
        self.textParentNumber3.setMaxLength(4)
        self.textYear.setMaxLength(4)
        self.textMonth.setMaxLength(2)
        self.textDay.setMaxLength(2)

        # 등록인지 수정인지에 따라 값 설정하기
        if what == "enroll":
            # primary key(id) 최대값 찾기, 없으면 1000000
            cs.execute("SELECT max(id) FROM student")
            mId = cs.fetchall()
            if mId[0][0] != None:
                mathId = int(mId[0][0])
                mathId += 1
            else:
                mathId = 1000000

            # 수정버튼 비활성화, ID에 신규 ID값 넣기
            self.btnupdate.setDisabled(True)
            self.textId.setText(str(mathId))

        elif what == "update":
            # 신규등록버튼 비활성화, ID에 선택된 셀의 id넣기
            self.btnnewenroll.setDisabled(True)
            self.textId.setText(str(mainId))

            # 등록일 칸 모두 비활성화
            self.textYear.setDisabled(True)
            self.textMonth.setDisabled(True)
            self.textDay.setDisabled(True)
            
            # 해당 id의 데이터 조회해오기
            cs.execute("SELECT * FROM student WHERE id =?", (mainId,))
            returnList = cs.fetchall()
            
            # 해당 데이터를 모달에 입력하기
            phone = str(returnList[0][7]).split('-')
            phone1 = phone[0]
            phone2 = phone[1]
            phone3 = phone[2]
            parPhone = str(returnList[0][10]).split('-')
            parPhone1 = parPhone[0]
            parPhone2 = parPhone[1]
            parPhone3 = parPhone[2]
            date = str(returnList[0][11]).split('-')
            textyear = date[0]
            textmonth = date[1]
            textday = date[2]
            self.textId.setText(str(returnList[0][0]))
            self.textName.setText(str(returnList[0][1]))
            self.comboSex.setCurrentText(str(returnList[0][2]))
            self.textAge.setText(str(returnList[0][3]))
            self.comboSchool.setCurrentText(str(returnList[0][4]))
            self.comboGrade.setCurrentText(str(returnList[0][5]))
            self.textSchoolName.setText(str(returnList[0][6]))
            self.textPhone1.setText(phone1)
            self.textPhone2.setText(phone2)
            self.textPhone3.setText(phone3)
            self.textParentName.setText(str(returnList[0][8]))
            self.comboParent.setCurrentText(str(returnList[0][9]))
            self.textParentNumber1.setText(parPhone1)
            self.textParentNumber2.setText(parPhone2)
            self.textParentNumber3.setText(parPhone3)
            self.textYear.setText(textyear)
            self.textMonth.setText(textmonth)
            self.textDay.setText(textday)

        # db close
        conn.close()

        # 버튼 클릭 이벤트 처리
        self.btnnewenroll.clicked.connect(lambda: self.btnEnroll())  # 인원 신규 등록
        self.btnupdate.clicked.connect(lambda: self.btnUpdate())  # 인원 정보 수정



    def btnEnroll(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # insert할 데이터 가공하기
            id = int(self.textId.text())
            name = self.textName.text()
            sex = self.comboSex.currentText()
            age = int(self.textAge.text())
            school = self.comboSchool.currentText()
            grade = self.comboGrade.currentText()
            schoolName = self.textSchoolName.text()
            number = self.textPhone1.text() + "-" + self.textPhone2.text() + "-" + self.textPhone3.text()
            parentName = self.textParentName.text()
            parentSex = self.comboParent.currentText()
            parentNumber = self.textParentNumber1.text() + "-" + self.textParentNumber2.text() + "-" + self.textParentNumber3.text()
            registDate = self.textYear.text() + "-" + self.textMonth.text() + "-" + self.textDay.text()

            if len(self.textMonth.text()) < 2:
                reply = QMessageBox.about(self, "Fail!!", "등록월을 '00'형식의 두글자로 입력해주세요. ex) 1월 -> 01")
                return
            if len(self.textDay.text()) < 2:
                reply = QMessageBox.about(self, "Fail!!", "등록일을 '00'형식의 두글자로 입력해주세요. ex) 1일 -> 01")
                return

            # 데이터 넣기
            insert_list = (
                (id, name, sex, age, school, grade, schoolName, number, parentName, parentSex, parentNumber, registDate, registDate)
            )
            cs.execute("INSERT INTO student(id, name, sex, age, school, grade, schoolName, number, parentName, parentSex, parentNumber, registDate, moneyDate) \
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", insert_list)

            # db close
            conn.close()
            
            # 성공메세지 출력
            reply = QMessageBox.about(self, "Success!!", "저장이 완료되었습니다.")

            # 창 종료
            self.close()
        except:
            reply = QMessageBox.about(self, "Error!!", "저장에 실패하였습니다.")
            traceback.print_exc()



    def btnUpdate(self):
        try:
            # db connect
            conn = sqlite3.connect("inmanage.db", isolation_level=None)
            cs = conn.cursor()

            # update할 데이터 가공하기
            id = int(self.textId.text())
            name = self.textName.text()
            sex = self.comboSex.currentText()
            age = int(self.textAge.text())
            school = self.comboSchool.currentText()
            grade = self.comboGrade.currentText()
            schoolName = self.textSchoolName.text()
            number = self.textPhone1.text() + "-" + self.textPhone2.text() + "-" + self.textPhone3.text()
            parentName = self.textParentName.text()
            parentSex = self.comboParent.currentText()
            parentNumber = self.textParentNumber1.text() + "-" + self.textParentNumber2.text() + "-" + self.textParentNumber3.text()

            # 데이터 넣기
            insert_list = (
                (name, sex, age, school, grade, schoolName, number, parentName, parentSex, parentNumber, id)
            )
            cs.execute("UPDATE student "
                        + "SET name = ?, sex = ?, age = ?, school = ?, grade = ?, schoolName = ?, "
                        + "number = ?, parentName = ?, parentSex = ?, parentNumber = ? "
                        + "WHERE id = ?", insert_list)

            # db close
            conn.close()

            # 성공메세지 출력
            reply = QMessageBox.about(self, "Success!!", "수정이 완료되었습니다.")

            # 창 종료
            self.close()
        except:
            reply = QMessageBox.about(self, "Error!!", "수정에 실패하였습니다.")
            traceback.print_exc()
