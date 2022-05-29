import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPalette
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QStackedLayout, QHBoxLayout, QFrame

from Planet import Planet


def read_texture(file: str):
    img = Image.open(file)
    img_data = np.array(list(img.getdata()), np.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


class GLPlanet(QGLWidget):
    def __init__(self, parent=None, width=250, height=200):
        QGLWidget.__init__(self, parent)
        self.texture_id = None
        self.setFixedSize(width, height)
        self.ug = 90
        self.on_focus = False
        self.parent = parent

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        if  self.on_focus:
            self.rot(0.5)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTranslate(0.0, 0.0, -60)
        glRotate(90, 1.0, 0.0, 0.0)
        glRotatef(self.ug, 0.0, 0.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        quadObj = gluNewQuadric()
        gluQuadricDrawStyle(quadObj, GLU_FILL)
        gluQuadricTexture(quadObj, GL_TRUE)
        gluSphere(quadObj, 20, 100, 100)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def initializeGL(self):
        self.qglClearColor(QColor(255, 255, 255))  # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)  # enable depth testing
        self.texture_id = read_texture(self.parent.planet.img_small_res)

    def rot(self, u):
        self.ug += u


class GLPlanetWindow(QGLWidget):
    def __init__(self, parent=None, width=600, height=600):
        QGLWidget.__init__(self, parent)
        self.texture_id = None
        self.setFixedSize(width, height)
        self.ug = 90
        self.parent = parent

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        self.rot(0.2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTranslate(0.0, 0.0, -70)
        glRotate(90, 1.0, 0.0, 0.0)
        glRotatef(self.ug, 0.0, 0.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        quadObj = gluNewQuadric()
        gluQuadricDrawStyle(quadObj, GLU_FILL)
        gluQuadricTexture(quadObj, GL_TRUE)
        gluSphere(quadObj, 20, 100, 100)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def initializeGL(self):
        self.qglClearColor(QColor(1, 14, 33))  # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)  # enable depth testing
        self.texture_id = read_texture(self.parent.planet.img_high_res)

    def rot(self, u):
        self.ug += u


class Card(QWidget):
    def __init__(self, parent, planet: Planet, ind):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(250, 300)
        self.planet = planet
        self.ind = ind
        self.parent = parent
        layout.addWidget(self.logoImg())
        layout.addWidget(self.logoText())
        layout.setContentsMargins(0, 10, 0, 10)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.transparent)
        rect = QRect()
        rect.setWidth(self.width())
        rect.setHeight(self.height() - 1)
        painter.drawRoundedRect(rect, 10, 10)

    def logoImg(self):
        self.planetGL = GLPlanet(self)
        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.planetGL.updateGL)
        timer.start()
        return self.planetGL

    def logoText(self):
        self.txt = QLabel(self)
        self.txt.setStyleSheet("background-color: white; padding: 0 0 0 20px")
        self.txt.setText(self.planet.name)
        self.txt.setFont(QFont('Courier', 18))
        return self.txt

    def enterEvent(self, QEvent):
        self.planetGL.on_focus = True

    def leaveEvent(self, QEvent):
        self.planetGL.on_focus = False

    def mouseReleaseEvent(self, QMouseEvent):
        self.parent.layout.setCurrentIndex(self.ind+1)


class Menu(QWidget):
    def __init__(self, parent, planets):
        super().__init__()
        self.width = parent.width - 30
        self.height = 700
        self.parent = parent
        self.arr = planets
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(30)
        self.setAttribute(Qt.WA_StyledBackground, True)
        for i in range(4):
            for j in range(3):
                if len(self.arr) > i * 3 + j:
                    card = Card(self.parent, self.arr[i * 3 + j], i * 3 + j)
                    layout.addWidget(card, i, j)
        self.setLayout(layout)
        self.setFixedWidth(self.width)


class Main(QWidget):
    def __init__(self, arr):
        super().__init__()
        self.layout1 = None
        self.title = 'StarrySky'
        self.width = 1000
        self.height = 655
        self.list = arr
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QStackedLayout()
        menu = Menu(self, self.list)
        mw = QScrollArea()
        mw.setWidget(menu)
        self.layout.addWidget(mw)
        for planet in self.list:
            pl = PlanetWindow(planet)
            pl.mouseReleaseEvent = lambda event: self.layout.setCurrentIndex(0)
            self.layout.addWidget(pl)
        self.setLayout(self.layout)
        self.setFixedSize(self.width, self.height)


class PlanetWindow(QWidget):
    def __init__(self, planet: Planet):
        super().__init__()
        self.planet = planet
        self.initUI()

    def initUI(self):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(1, 14, 33))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.layout = QHBoxLayout()
        self.planetGL = GLPlanetWindow(self)
        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.planetGL.updateGL)
        timer.start()
        self.layout.addWidget(self.planetGL)
        self.info = PlanetInfo(self.planet)
        mw = QScrollArea()
        mw.setFrameShape(QFrame.NoFrame)
        mw.setWidget(self.info)
        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.info.repaint)
        timer.start()
        self.layout.addWidget(mw)
        self.setLayout(self.layout)


class PlanetInfo(QWidget):
    def __init__(self, planet: Planet):
        super().__init__()
        self.planet = planet
        self.setFixedWidth(360)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(1, 14, 33))
        self.setPalette(pal)
        l = QLabel()
        l.setText(self.planet.name)
        l.setStyleSheet("color: white; padding: 0 0 10 0px")
        l.setFont(QFont('Courier', 24))
        self.layout.addWidget(l)
        r = self.planet.get_dynamic_data()
        array = [f'Количество спутников: {self.planet.number_of_moons}',
                 f'Средняя температура: {self.planet.temperature}\u00b0', f'Радиус: {self.planet.radius} км',
                 f'Масса: {self.planet.mass} кг', f'Объём: {self.planet.volume} км\u00b3',
                 f'Расстояние до Земли: \n\t{r if r else 0} а.е.']
        for i in array:
            rev = QLabel()
            rev.setText(i)
            rev.setStyleSheet("color: white; padding: 5 0 0 5px")
            rev.setFont(QFont('Courier', 12))
            self.layout.addWidget(rev)
        self.setLayout(self.layout)
