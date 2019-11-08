# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import threading

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication

from Ui_main import Ui_MainWindow
from selenium import webdriver
import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle)

    def show_info(self, str):
        self.textBrowser.append(str)
        self.textBrowser.moveCursor(QTextCursor.End)

    def handle(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        t = threading.Thread(target=self.qiang)
        t.setDaemon(True)
        t.start()

    def qiang(self):
        self.show_info('开始秒杀')
        while 1:
            try:
                if self.driver.find_element_by_link_text('立即购买'):
                    self.driver.find_element_by_link_text('立即购买').click()
                    break
            except Exception:
                pass
        while 1:
            try:
                if self.driver.find_element_by_link_text('提交订单'):
                    self.driver.find_element_by_link_text('提交订单').click()
                    break
            except Exception:
                pass

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        self.url = 'https://www.taobao.com/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.driver.get(self.url)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        print(self.driver.page_source)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        '''理肤泉官方旗舰店'''
        no = 5
        print(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # self.timer.singleShot(1000* 30 ,self.handle)
        try:
            if self.driver.find_element_by_class_name('tb-btn-wait'):
                self.show_info('已找到秒杀目标')
                target_time = self.driver.find_element_by_class_name('tm-countdown-timer').text
                self.show_info('秒杀目标将于' + target_time + '后开始,请保持网络畅通...')
                target_time = target_time.split('小时')
                hour, min = target_time[0], target_time[1].split('分')[0]
                now_date = datetime.datetime.now()
                if int(min) < no:
                    hour = int(hour) - 1
                    min = int(min) + 60 - no
                else:
                    hour = int(hour)
                    min = int(min) - no
                date = hour * 60 + min
                self.timer.singleShot(1000 * 60 * date, self.handle)
                self.pushButton_3.setDisabled(True)

        except Exception:
            self.show_info('未找到秒杀目标')


def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
