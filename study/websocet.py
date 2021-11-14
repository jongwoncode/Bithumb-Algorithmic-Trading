import sys
import time
import pybithumb
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QProgressBar
# 테이블에 표현될 데이터를 정의하기 위한 모듈을 import한다.
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from PyQt5.QtWidgets import QApplication

class OrderbookWidget(QWidget):
    def __init__(self, parent=None, ticker = 'BTC'):
        super().__init__(parent)
        uic.loadUi('resource/orderbook.ui', self)
        self.ticker = ticker

        for i in range(self.tableBids.rowCount()):
            # 매도 호가 테이블의 1열에 저장될 문자열 객체를 생성하고 오른쪽 정렬한다.
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 0, item_0)

            # 메도 호가 테이블의 2열에 저장될 문자열 객체를 생성하고 오른쪽 정렬한다.
            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 1, item_1)

            # 3열에 저장될 호가 잔량을 시각화 하기 위한 QProgressBar 객체를 생성한다.
            item_2 = QProgressBar(self.tableAsks)
            # QProgressBar에 출력될 텍스트는 가운데 정렬한다.
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            ## CSS로 셀의 배경 색상을 흰색, ProgressBar의 게이지를 투명도가 부여된 빨강으로 지정.
            item_2.setStyleSheet('''
            QProgressBar {background-color : rgba(0, 0, 0, 0%); border : 1}
            QProgressBar :: Chunk {background-color : rgba(255, 0, 0, 50%); border : 1}
            ''')
            # 객체를 테이블의 3열에 저장한다.
            self.tableAsks.setCellWidget(i, 2, item_2)

            # 매수 호가
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 1, item_1)

            item_2 = QProgressBar(self.tableBids)
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_2.setStyleSheet('''
            QProgressBar {background-color : rgba(0, 0, 255, 0%);border : 1} 
            QProgressBar::Chunk {background-color : rgba(255, 0, 0, 50%); border : 1}
            ''')
            self.tableBids.setCellWidget(i, 2, item_2)

        # OrderbookWidget의 생성자에서 OrderbookWorker를 생성하고 dataSent 시그널을 연결할 슬롯을 정의한다.
        # 데이터를 얻어오는 QThread를 실행한다.
        self.ow = OrderbookWorker(self.ticker)
        self.ow.dataSent.connect(self.updateData)
        self.ow.start()


    # QThread에서 시그널이 전송되면 updateData가 실행된다.
    # 얻어온 orderbook 데이터를 콘솔이 아닌 GUI 창에 연결한다.
    def updateData(self, data):
        tradingValues = []
        for v in data['bids']:
            tradingValues.append(int(v['price']*v['quantity']))

        maxTradingValue = max(tradingValues)

        for i, v in enumerate(data['asks'][::-1]):
            item_0 = self.tableAsks.item(i,0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableAsks.item(i, 1)
            item_1.setText(f"{v['quantity']:,}")
            item_2 = self.tableAsks.cellWidget(i, 2)
            item_2.setRange(0, maxTradingValue)
            item_2.setFormat(f"{tradingValues[i]:,}")
            item_2.setValue(tradingValues[i])

        for i, v in enumerate(data['bids']):
            item_0 = self.tableBids.item(i,0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableBids.item(i, 1)
            item_1.setText(f"{v['quantity']:,}")
            item_2 = self.tableBids.cellWidget(i, 2)
            item_2.setRange(0, maxTradingValue)
            item_2.setFormat(f"{tradingValues[i]:,}")
            item_2.setValue(tradingValues[i])


    # Qhtread의 종룔를 처리하기 위해 QWidget의 메서드를 오버라이딩합니다.
    # 메인 위젯이 종료될 때 closeEvent 메서드가 실행됩니다.
    def closeEvent(self, data):
        self.ow.close()



# 데이터를 얻어오는 OrderbookWorker 스레드를 정의
class OrderbookWorker(QThread):
    dataSent = pyqtSignal(dict)     # dict를 반환하는 dataSent 시그널을 정의한다.

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            data = pybithumb.get_orderbook(self.ticker, limit=10)  # 공개 API를 사용해서 orderbook을 매수/매도 각각 10개씩 얻어온다.
            time.sleep(0.05)  # 초당 20번의 요청을 수행.
            self.dataSent.emit(data)

    def close(self):
        self.alive = False





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ow = OrderbookWidget(ticker='BTC')
    ow.show()
    exit(app.exec_())