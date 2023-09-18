import sys
from PySide6 import QtWidgets
from segtumor import Segtumor

app = QtWidgets.QApplication(sys.argv)
window = Segtumor()
window.show()

app.exec()