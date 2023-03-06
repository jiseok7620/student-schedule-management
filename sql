1. 인원테이블(student)
CREATE TABLE IF NOT EXISTS student
:id(primary key), 이름(name), 성별(sex), 나이(age), 학교(school), 학년(grade), 주소(address1), 상세주소(address2),
이메일(email), 전화번호(number),부모님성명(parentName), 부모님성별(parentSex), 부모님번호(parentNumber), 등록일(registDate)

2. 인원당 사용교재테이블(textbookperman)
CREATE TABLE IF NOT EXISTS textbookperman
:id(foreign key), book1, book2, book3, book4, book5, book6, book7, book8, book9, book10

3. 진도 테이블
CREATE TABLE IF NOT EXISTS progress
:id(foreign key), 교재명(bookname), 시작페이지(startPage), 끝페이지(endPage), 일시(datetime)

4. 교재 테이블(textbook)
CREATE TABLE IF NOT EXISTS textbook
:교재id(bookid)(PRIMARY KEY), 교재명(bookname), 대단원명(subjectName), 부단원(subjectName2), 시작페이지(startPage), 끝페이지(endPage), 총페이지수(allPage),
학교(school), 학년(grade)

5. 스케줄관리 테이블
CREATE TABLE IF NOT EXISTS schedule
 :id(foreign key), 번호(NO), 내용1(text1), 내용2(text2), 내용3(text3), 구분(remark), 일시(datetime)