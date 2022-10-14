import sys
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie
from random import randint

class Mole(QtWidgets.QMainWindow):
    def __init__(self, xy, size=0.2, on_top=False):
        super(Mole, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = ".\\..\\images\\mole.gif"
        self.xy = xy
        self.size = size
        self.on_top = on_top
        self.setupUi()
        self.show()

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint |QtCore.Qt.Tool| QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        self.label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        self.setGeometry(self.xy[0], self.xy[1], w, h)

    def mouseMoveEvent(self, e):
        return [e.globalX(), e.globalY()]
    
    def mousePressEvent(self,e):
        self.moveto(self.xy,self.mouseMoveEvent(),1.5)
    
    def keyPressEvent(self, e):
        if e.key()==32:
            toxy = [randint(0,1700),randint(0,700)]
            m.moveto(self.xy,toxy,1.5)

    def moveto(self, from_xy, to_xy, v):
        self.v = v
        self.vx = int((to_xy[0]-from_xy[0])/(100*t))
        self.vy = int((to_xy[1]-from_xy[1])/(100*t))
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.movemove)
        self.changetohole()
        self.timer.start()
    
    def movemove(self):
        self.t -= 0.01
        if self.t<=0:
            self.timer.stop()
            self.changetomole()
        self.xy[0] += self.vx
        self.xy[1] += self.vy
        self.move(*self.xy)

    def changetohole(self):
        self.img_path = ".\\..\\images\\hole.gif"
        self.setupUi()
        self.show()
    
    def changetomole(self):
        self.img_path = ".\\..\\images\\mole.gif"
        self.setupUi()
        self.show()

if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)
    app = QtWidgets.QApplication(sys.argv)
    m = Mole(xy=[randint(0,1700),randint(0,700)], on_top=True)
    sys.exit(app.exec_())
