import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter    # Antialiasing을 제거하는데 사용되는 모듈을 import 한다.
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
        # QLineSeries : 차트에 표현될 데이터를 관리한다(도화지에 그려진 선)
        # QChart : 데이터가 그려질 공간(도화지)
from PyQt5.QtCore import Qt, QDateTime

import time
import pybithumb
from PyQt5.QtCore import QThread, pyqtSignal


class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker='BTC'):
        super().__init__(parent)
        uic.loadUi('resource/chart.ui', self)
        self.ticker = ticker
        self.viewLimit = 120 # 라인 차트로 그릴 데이터의 수를 미리 정의

        # QLineSeries 객체의 append메서드로 출력할 데이터의 좌표를 x, y 순서대로 입력한다.
        #(0, 10), (1, 20), (2, 10) 세개의 포인트를 추가
        self.priceData = QLineSeries()
        # 데이터를 차트 객체로 전달해서 시각화 한다./ QChart를 사용해 차트의 타이틀을 입력하거나 범례를 추가하는 등의 일을 할 수 잇따.
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceView.setChart(self.priceChart)
        self.priceChart.legend().hide()  # 차트의 범례를 숨긴다.


        # 차트 축 설정하는 부분
        axisX = QDateTimeAxis()      # PyChart에서 날짜 축을 관리하는 QDateTimeAxis 객체를 생성합니다.
        axisX.setFormat('hh:mm:ss')  # 날짜는 시:분:초 형태로 차트에 표시합니다.
        axisX.setTickCount(4)        # 차트에 표시할 날짜의 개수를 4로 지정합니다.
        dt = QDateTime.currentDateTime()  # 현재 시간 정보를 QDataTime 객체로 언어온다.
        axisX.setRange(dt, dt.addSecs(self.viewLimit)) # X축에 출력될 값의 범위를 현재 시간부터 viewLimit(120)초 이후까지 설정합니다.
                                                        # addSecs 메서드는 지정된 초 이후의 시간을 QDateTime으로 반환합니다.

        # 정수를 저장하는 축을 생성하고 축의 레이블을 차트에 표시하지 않습니다.
        axisY = QValueAxis()
        axisY.setVisible(False)

        # 생성한 X, Y축을 차트와 데이터에 연결합니다.
        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)

        # 차트 객체 안에 여백을 최소화해서 차트를 크게 그립니다. 왼쪽/위쪽/오른쪽/아래쪽 여백을 0으로 설정하라는 의미.
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)


        # 차트를 ui에서 그려놨던 priceView로 출력한다.
        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing) # 차트에 anti-aliasing을 적용

        ## 메인 위젯에서 PriceWorker 객체를 생성하고 dataSent 이벤트를 연결할 슬롯을 지정한다.
        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()

    ## PriceWorker 스레드의 올바른 종룔를 위해 closeEvent 메서드를 정의한다.
    ## 부모 QWidget에 정의된 메서드로 UI의 종료 버튼을 누르면 실행.
    ## 자식 클래스에서 closeEvent를 재정의해서 종료되기 전 스레드를 종요한다./ (메서드 오버라이딩)
    def closeEvent(self, event):
        self.pw.close()


    # 차트에 그릴 데이터를 입력받는 appendData 메서드. 데이터는 QLineSeries에 viewLimit(120)개 까지 저장한다.
    # 만약 120개의 데이터가 저장돼 있다면 오래된 데이터 하나 제거하고 새로운 데이터를 추가한다.
    def appendData(self, currPrice):
        if len(self.priceData) == self.viewLimit:    # 정해진 데이터 개수만큼 저장돼 있다면 오래된 0번 인덱스의 데이터를 삭제한다.
            self.priceData.remove(0)   # QLineSeries 객체의 remove 메서드는 인덱스를 입력받아 데이터를 제거한다.

        # 현재 시간 정보를 얻어와서 시간과 현재가(currPrice)를 함께 저장
        dt = QDateTime.currentDateTime()
        self.priceData.append(dt.toMSecsSinceEpoch(), currPrice) # append 메서드는 millisecond(ms)를 입력받으므로,
        self.__updateAxis()                                       #toMSecsSinceEpoch() 메서드로 QDateTime 객체를 millisecond로 변환
        # 차트의 축정보를 업데이트하는 __updateAxis() 메서드를 호출. 실시간으로 추가되는 데이터의 위치를 지정.

    ## __updateAxis 메서드 추가. 데이터가 실시간으로 입력되면 X, Y축 정보를 조절해서 어느 구간을 출력할지 결정
    def __updateAxis(self):
        pvs = self.priceData.pointsVector() # pointsVecotr 메서드를 사용해서 QLineSeries 객체에 저장된 데이터를 리스트로 얻어 온다.
                                            # pvs에 저장된 리스 안에는 QPointF 객체로 위치 정보가 저장돼 있다.
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x())) # 가장 오래된 데이터 [0번 인덱스] 꺼내와서 x 좌표에 저장된 값을 가져온다.
                            # fromMSecsSinceEpoch : MS -> HH:MM:SS 형태로 바꿔준다./ QDateTime 객체로 변환한다.
        if len(self.priceData) == self.viewLimit :
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x())) # 최근 시간 정보를 가져온다. QDateTime 객체로 반환
        else:
            dtLast = dtStart.addSecs(self.viewLimit)  # 최근 시간 +(addSecs)[self.viewLimit = 120초]를 마지막 시간으로 설정해준다.
            # 데이터 개수가 viewLimit보다 작다면 시작 위치 0번을 기준으로 viewLimit 초 이후까지 출력한다.

        # 앞에서 얻어온 위치 정보를 보여줄 수 있도록 X축의 번위를 설정한다.
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)


        # QPontF 객체에서 y 좌표를 가져와서 최솟값, 최댓값으로 Y축에 표시될 범위를 지정합니다.
        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))




## 데이터를 얻어와서 차트와 연결해주는 부분.
class PriceWorker(QThread): # QThread를 상속받은 PriceWorker 클래스를 정의한다.
    dataSent = pyqtSignal(float) # 메인 스레드에 데이터를 전달하기 위한 dataSent 시그널을 정의한다.

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True    # QThread를 안전하게 종료하기 위해 인스턴스 변수를 사용한다. alive의 초기값을 True입니다.

    # close 함수가 실행되기 전까지 데이터를 받아오고, 시그널을 내보낸다.
    def run(self):
        while self.alive :
            data = pybithumb.get_current_price(self.ticker)
            time.sleep(0.5)
            self.dataSent.emit(data)

    # 메인 스레드에서 close 메서드가 호출되면, PriceWorker 스레드의 종료를 의미한다.
    def close(self):
        self.alive = False





if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())


