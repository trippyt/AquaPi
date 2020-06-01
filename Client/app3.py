import sys
import asyncio
from PyQt5 import QtCore, QtWidgets, uic
import aioschedule as schedule

from asyncqt import QEventLoop, asyncSlot, asyncClose

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout)


class MainWindow(QWidget):
    """Main window."""

    def __init__(self):
        super().__init__()
        uic.loadUi('myform.ui', self)
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sch_run)
        self.timer.start()
        schedule.every().second.do(self.test)

    @asyncSlot()
    async def sch_run(self):
        print('Async...')

    async def test(self):
        print('test...')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    mainWindow = MainWindow()
    mainWindow.show()

    with loop:
        sys.exit(loop.run_forever())
