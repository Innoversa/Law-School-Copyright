from PyQt5.QtWidgets import *
from controller import controller
import sys
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
import traceback, sys
import multiprocessing


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    main_window = controller()
    main_window.show()
    sys.exit(app.exec_())