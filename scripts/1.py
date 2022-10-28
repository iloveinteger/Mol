import sys
import os
import mouse
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie
from random import randint
from time import sleep

class loopp(QtCore.QThread):
    domove = QtCore.pyqtSignal(list)

    def run(self):
        global stat
        while True:
            if mouse.is_pressed("right") and stat == 'm':
                to_xy = list(mouse.get_position())
                print(to_xy)
                self.domove.emit(to_xy)
                sleep(0.1)

class Mole(QtWidgets.QMainWindow):
    def __init__(self, xy, size=0.2, on_top=False):
        super(Mole, self).__init__()
        global stat
        stat = 'm'
        self.loopp = loopp()
        self.loopp.start()
        self.loopp.domove.connect(lambda x : self.moveto(self.xy,x,1))
        self.img_path = ".\\..\\images\\mole.gif"
        self.xy = xy
        self.size = size
        self.on_top = on_top
        self.setupUi()

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

    def keyPressEvent(self, e) :
        if (e.key() == QtCore.Qt.Key_Escape):
            self.close()
            QtCore.QCoreApplication.instance().quit()
        
    def moveto(self, from_xy, to_xy, t):
        global stat
        stat = 'h'
        self.t = t
        self.vx = int((to_xy[0]-from_xy[0])/(100*t))
        self.vy = int((to_xy[1]-150-from_xy[1])/(100*t))
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
            global stat
            stat = 'm'
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
    m.show()
    sys.exit(app.exec_())
