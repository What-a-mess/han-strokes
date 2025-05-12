import logging
import time
import os
import sys
import traceback
from PyQt5 import QtWidgets
from gui import MainWindow

from common import Storage


os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.INFO)
logging.basicConfig(filename=f"logs/{str(time.time())}.log",level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def error_handler(etype, value, tb):
    error_msg = ''.join(traceback.format_exception(etype, value, tb))
    logger.error(error_msg)
    
sys.excepthook = error_handler

config = Storage("config.json", 5)
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(config)
window.show()
app.exec()
config.close()