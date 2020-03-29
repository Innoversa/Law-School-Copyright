from PyQt5.QtWidgets import *
from ui.qtsrc.controller import controller
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = controller()
    main_window.show()
    sys.exit(app.exec_())