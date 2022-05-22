import sys

from PyQt5.QtWidgets import QApplication
from wind import Main
from planet_request import planet_list_generator

if __name__ == '__main__':
    arr = planet_list_generator()
    app = QApplication(sys.argv)
    ex = Main(arr)
    ex.show()
    sys.exit(app.exec_())