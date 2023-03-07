@echo off
chcp 65001

rem python
IF %ERRORLEVEL%=="0" (
    echo 파이썬이 정상적으로 설치되어있습니다.
) ELSE (
    echo 실패... 파이썬을 설치해주세요.
)

rem step1. 환경변수 설정
set path=%path%;C:\Users\A226U\AppData\Local\Programs\Python\Python310;
set path=%path%;C:\Users\A226U\AppData\Local\Programs\Python\Python310\Scripts;

rem step2. 실행에 필요한 파이썬 모듈 설치
pip install pyqt5

rem step3. 실행
cd D:\automatic\studentmanage
python main.py
pause


