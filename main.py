import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from wind import Main
from planet_request import planet_list_generator


if __name__ == '__main__':
    # generation of the celestial bodies' list
    arr = planet_list_generator()
    # the app's launch
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    ex = Main(arr)
    ex.show()
    sys.exit(app.exec_())
