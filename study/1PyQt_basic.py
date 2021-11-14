#1. PyQT basic

'''
PyQt5로 프로그래밍을 작성할 때는 일반적으로 다음의 두 가지가 필요하다
0. Anaconda3\Library\bin\designer.exe
1. QApplication 클래스의 인스턴스
2. 이벤트 루프 -> X를 누르기 전 까지 실행되도록 무한 반복 해주는 것. / QApplication 클래스의 exec_()메서드를 통해서 호출한다.

3. 버튼과 같은 컴포넌트를 PyQt에서 위젯이라고 부른다. 우리는 원하는 위젯을 불러다가 설치하면 되는 것이다.
4. 다른 위젯에 포함되지 않은 최상위 위젯을 특별히 윈도우라고 부른다.
5. 화면에 여러 위젯을 동시 출력하기 위해서는 class로 구성하는 것이 편하다.
6. 클래스를 상속 받을 때는 PyQt에서 제공하는 메인 클래스(QMainWindow)를 상속 받는다.  항상 부모 클래스의 생성자를 호출해야한다. 

-- 함수 표기 --
1. 윈도우 : QMainWindow, QDialog/ PyQt에서 제공하는 메일 클래스
2. 버튼 위젯 : QPushButton('문자', '버튼이 위치하는 윈도우')
    2.1 버튼 이동 : btn.move(x, y)
    2.2 버튼에 발생하는 이벤트(clicked)와, 메서드(self.btn_clicked) 바인딩(connect) : btn.clicked.connect(self.btn_clicked)
3. 라벨 위젯 : QLabel()
4. 보여 줘라 : show()  / QMainWindow의 메서드이다.
5. 이벤트 루프 생성 : exec_()
    5.1 QApplication() 객체를 생성한 후 exec_()메서드를 호출하면 이벤트 루프가 생성되는데 이벤트 루프는 루프를 돌고 있다가 사용자가 이벤트를 발생시키면
        이벤트에 연결된 메서드를 호출해주는 역할을 한다./ 이벤트 루프가 직접 호출하기 때문에, 호출 되는 메서드들은 call back 함수라고 부른다.
6. 크기 지정 : setGeometry(좌표)
7. 윈도우 제목 : setWindowTitle()
8. 이미지 넣기 : setWindowIcon(QIcon( )) / from PyQt5.QtGui import * 해줘야 한다.
8. 글씨 입력 라인에 글씨 넣기 : lineEdit.setText(str(price))   # lineEdit 객체에 setText()메서드를 통해 문자를 표시
9. 일정 시간마다 작업 반복 : QTimer
    9.1 timeout() 메서드 : 설정한 interval 마다 발생하는 매서드
    9.2 currentTime() : 현재 시각 -> 문자열 변환, 윈도우 상태바에 출력
10. self.statusBar().showMessage(str_time)  # 상태창에 띄우기
'''
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # 위젯 생성 코드
#         self.setGeometry(100, 200, 300, 400)
#         self.setWindowTitle('PyQt')
#         self.setWindowIcon(QIcon('titleicon.png'))
#
#         btn = QPushButton('Button1', self)
#         btn.move(10, 10)
#         btn.clicked.connect(self.btn_clicked)           #2.2 버튼에 발생하는 이벤트(clicked)와, 메서드(self.btn_clicked) 바인딩(connect)
#
#         btn2 = QPushButton('Button2', self)
#         btn2.move(10, 40)
#
#     ## 이벤트에 해당하는 메서드(connect로 바인딩 해주는 부분)
#     def btn_clicked(self):
#         print('버튼 클릭')
#
#

# QApplication 객체 생성 및 이벤트 루프 생성 코드
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()

###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
'''
Ui 파일 불러오기
1. from PyQt5 import uic    해준다.
2. uic.loadUiType('mywindow.ui')[0]/ uic 모듈의 loadUiType() 메서드는 Qt Designer의 결과물을 읽어서 파이썬 클래스 코드를 만든다.
        mywindow.ui 파일은 XML 코드로 되어 있다. 이를 파이썬 코드로 변경해주는 것.
3. self.setupUi : form_class에 정의된 메서드로 QtDesigner에서 만든 클래스들을 초기화한다.


'''

#
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5 import uic                                   ## 생성한 ui 불러오려면 임포트
# from PyQt5.QtCore import *          # QTime 클래스 사용하기 위함
# import pykorbit
#
#
#
# form_class = uic.loadUiType('window.ui')[0]
#
# class MyWindow(QMainWindow, form_class):        # 다중 상속 받는 구조
#     def __init__(self):
#         super().__init__()
#         # ui 정규화 코드
#         self.setupUi(self)
#
#
#         self.timer = QTimer(self)   # Qtimer 인스턴스 생성
#         self.timer.start(1000)
#
#         ## 바인딩 해주는 부분
#         self.timer.timeout.connect(self.Bprice_time)   # 시간
#
#
#     ## 이벤트에 해당하는 메서드
#     def Bprice_time(self):
#         cur_time = QTime.currentTime()
#         str_time = cur_time.toString('hh:mm:ss')
#         self.statusBar().showMessage(str_time)  # 상태창에 띄우기
#
#         price = pykorbit.get_current_price('BTC')
#         self.bprice.setText(str(price))  # lineEdit.setText(str(price))   # lineEdit 객체에 setText()메서드를 통해 문자를 표시
#
#
# # QApplication 객체 생성 및 이벤트 루프 생성 코드
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
'''
1. PyQt는 위젯에 정의된 이벤트를 시그널(signal)이라고 부르고 이벤트가 발생할 때 호출되는 함수나 메소드를 슬롯(slot)이라고 부른다.
2. 시그널이 발생할 때 슬롯이 호출되도록 하려면 다음과 같이 연결을 한다.
btn.clicked.connect(self.btn_clikced)
3. 여기서 click은 왼쪽, 오른쪽 마우스 구분 없다 -> 이런것까지 구분할 수 있는 사용자 정의 signal을 만들 수 있다.

[1. 시그널 만들기 -> 2.emit()메소드로 시그널 발생하는 함수 만들기-> 3.시그널과 매서드를 바인딩 -> 4. 시그널 발생 개시]

4.@pyqtSlot()             # 시그널과 슬롯을 연결할 때 데커레이터를 적어주면 더 좋다./ @pyqtSlot()은 특정 시점에서 클래스와 클래스 사이의 데이터 이동을 원활하게 해준다.
'''

# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
# class MySignal(QObject):        # 사용자 시그널을 정의하기 위해 MySignal 클래스를 정의
#     signal1 = pyqtSignal        # pyqtSignal의 인스턴스 생성(시그널을 만드는 것 같다.)
#
#     def run(self):
#         self.signal1.emit()     # emit() 메소드를 호출하여 시그널을 발생시킨다.
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super.__init__()
#
#         mysignal = MySignal()   # MySignal 클래스에서 mysignal이라는 인스턴스 생성, 시그널 이름인듯.
#         mysignal.signal1.connect(self.signal1_emitted)      # 시그널과 메서드를 묶어준다.
#         mysignal.run()  # 시그널 발생
#
#     @pyqtSlot()             # 시그널과 슬롯을 연결할 때 데커레이터를 적어주면 더 좋다.
#     def signal1_emitted(self):          # 사용자 정의 시그널을 방출 시켰을 때 호출되는 메소드를 정의
#         print('signal1 emitted')
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()

##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
'''
시그널을 통해서 한 객체로부터 다른 객체로 값을 보내는 것이다.
가상화페 금액 조회기 같은 프로그램을 만들 때 한 클래스에서는 금액을 조회하고 다른 클래스에서는 조회된 값을 GUI에 값을 출력하는 경우가 있다.
이 경우 금액을 조회하는 역할의 클래스는 금액 조회가 완료되자마자 시그널을 발생시키면 된다.
'''
#
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
#
# class MySignal(QObject):
#     signal1 = pyqtSignal()
#     signal2 = pyqtSignal(int, int)
#
#     def run(self):
#         self.signal1.emit()
#         self.signal2.emit(1, 2)
#
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         mysignal = MySignal()
#         mysignal.signal1.connect(self.signal1_emitted)
#         mysignal.signal2.connect(self.signal2_emitted)
#         mysignal.run()
#
#     @pyqtSlot()
#     def signal1_emitted(self):
#         print("signal1 emitted")
#
#     @pyqtSlot(int, int) # 전달하는 데이터 타입을 정의
#     def signal2_emitted(self, arg1, arg2):
#         print("signal2 emitted", arg1, arg2)
#
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# app.exec_()


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
'''
API를 사용해서 데이터 받아오기
'''
# import requests
# import datetime
#
# r = requests.get('http://api.korbit.co.kr/v1/ticker/detailed?currency_pair=btc_krw')
# bitcoin = r.json()  # 출력되는 형태는 겉으로는 dict 형태 같지만 실제로는 문자열, 따라서 .json()해주면 dict로 바뀜
#
# timestamp = bitcoin['timestamp']
# date = datetime.datetime.fromtimestamp(timestamp/1000)  #timestamp 항목은 최종 체결 시각을 의미, 일반적으로 1970/1/1일 부터 지난 시간(초)를 의미
# print(date)                                                         # 사람이 읽을 수 있게 변경하려면 datetime 모듈을 쓴다.






