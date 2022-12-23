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
        timer = 100000
        while True:
            if mouse.is_pressed("left") and stat == 'm':
                to_xy = list(mouse.get_position())
                print("toxy",to_xy)
                self.domove.emit(to_xy)
                sleep(0.3)
            else:
                if timer<0:
                    sleep(0.1)
                    to_xy = [0,0]
                    to_xy[0] = randint(100,1000)
                    to_xy[1] = randint(100,700)
                    print(to_xy)
                    self.domove.emit(to_xy)
                    timer = randint(100000000,1000000000)
                timer -= 1

class Mole(QtWidgets.QMainWindow):
    def __init__(self, xy, size=1, on_top=False):
        super(Mole, self).__init__()
        global stat
        stat = 'm'
        self.loopp = loopp()
        self.loopp.start()
        self.loopp.domove.connect(lambda x : self.reaction(self.xy,x,1))
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

    def reaction(self, from_xy, to_xy, t):
        print("xy",self.xy)
        x = self.xy[0]
        y = self.xy[1]
        to_xy[0] += -140
        to_xy[1] += -120
        if x-100<to_xy[0]<x+100 and y-100<to_xy[1]<y+100:
            r = randint(0,100)
            self.mood_change(r)
            print(r)
        else:
            self.changetohole()
            global stat
            stat = 'h'
            self.t = t
            self.uptime = 0.6
            self.vx = (to_xy[0]-from_xy[0])//(100*t)
            self.vy = (to_xy[1]-from_xy[1])//(100*t)
            self.lx = (to_xy[0]-from_xy[0])%(100*t)
            self.ly = (to_xy[1]-from_xy[1])%(100*t)
            self.timer = QtCore.QTimer(self)
            self.timer.setInterval(10)
            self.timer.timeout.connect(self.movemove)
            self.move(*self.xy)
            self.timer.start()

    def movemove(self):
        self.uptime -= 0.01
        if self.t==0:
            self.xy[0] += self.lx
            self.xy[1] += self.ly
        elif self.t<0:
            self.timer.stop()
            self.changetomole()
            global stat
            stat = 'm'
        elif self.uptime>=0:
            pass
        else:
            self.t -= 0.01
            self.xy[0] += self.vx
            self.xy[1] += self.vy
            self.move(*self.xy)
    
    def changetohole(self):
        self.img_path = ".\\..\\images\\mol_down.gif"
        movie = QMovie(self.img_path)
        self.label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
    
    def changetomole(self):
        self.img_path = ".\\..\\images\\mol_up.gif"
        movie = QMovie(self.img_path)
        self.label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        movie.finished.connect(self.mol_idle)

    def mol_idle(self):
        self.img_path = ".\\..\\images\\mole.gif"
        movie = QMovie(self.img_path)
        self.label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

    def mood_change(self,n):
        if (n%2) == 1:
            self.img_path = ".\\..\\images\\mol_surprised.gif"
            movie = QMovie(self.img_path)
            self.label.setMovie(movie)
            movie.start()
            movie.stop()
            w = int(movie.frameRect().size().width() * self.size)
            h = int(movie.frameRect().size().height() * self.size)
            movie.setScaledSize(QtCore.QSize(w, h))
            movie.start()
            movie.finished.connect(self.mol_idle)
        else:
            self.img_path = ".\\..\\images\\mol_angry.gif"
            movie = QMovie(self.img_path)
            self.label.setMovie(movie)
            movie.start()
            movie.stop()
            w = int(movie.frameRect().size().width() * self.size)
            h = int(movie.frameRect().size().height() * self.size)
            movie.setScaledSize(QtCore.QSize(w, h))
            movie.start()
            movie.finished.connect(self.mol_idle)

    def keyPressEvent(self, e):
        key = e.key()
        if key == QtCore.Qt.Key.Key_Escape:
            quit()
        
if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)
    app = QtWidgets.QApplication(sys.argv)
    m = Mole(xy=[randint(0,1700),randint(0,700)], on_top=True)
    m.show()
    sys.exit(app.exec_())
