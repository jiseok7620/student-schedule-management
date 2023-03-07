import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def btnsearchClick(self, conSchool, conGrade):
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        if conSchool == "전체":
            cs.execute("SELECT * FROM student")
            returnList = cs.fetchall()

            # db close
            conn.close()

            return returnList

    def btndeleteClick(self, mainid, mainname):
        conn = sqlite3.connect("inmanage.db", isolation_level=None)
        cs = conn.cursor()

        reply = QMessageBox.question(self, '경고창!!', '정말로 ' + mainname + '을 지우시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            cs.execute("DELETE FROM student WHERE id = ?", (mainid,))
        else:
            pass

        # db close
        conn.close()
