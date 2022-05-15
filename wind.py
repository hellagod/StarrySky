import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QStackedLayout


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
    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.texture_id = None
        self.setFixedSize(250, 200)
        self.ug = 90
        self.on_focus = False

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        if self.on_focus:
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
        self.texture_id = read_texture('moon_1.jpg')

    def rot(self, u):
        self.ug += u


class Card(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(250, 300)
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
        self.planet = GLPlanet(self)
        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.planet.updateGL)
        timer.start()
        return self.planet

    def logoText(self):
        self.txt = QLabel(self)
        self.txt.setStyleSheet("background-color: white; padding: 0 0 0 20px")
        self.txt.setText('Планета')
        self.txt.setFont(QFont('Arial', 18))
        return self.txt

    def enterEvent(self, QEvent):
        self.planet.on_focus = True

    def leaveEvent(self, QEvent):
        self.planet.on_focus = False


class Menu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.width = parent.width - 50
        self.height = 700
        self.initUI()
        self.parent = parent

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(30)
        self.setAttribute(Qt.WA_StyledBackground, True)
        arr = ['Меркурий', 'Венера', 'Земля', 'Марс', 'Юпитер', 'Сатурн', 'Уран', 'Нептун', 'Плутон']
        for i in range(3):
            for j in range(3):
                if len(arr) > i * 3 + j:
                    card = Card()
                    card.mouseReleaseEvent = lambda event: self.parent.layout.setCurrentIndex(1)
                    layout.addWidget(card, i, j)
        self.setLayout(layout)
        self.setFixedWidth(self.width)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'StarrySky'
        self.width = 1000
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QStackedLayout()
        menu = Menu(self)
        pl = PlanetWindow()
        pl.mouseReleaseEvent = lambda event: self.layout.setCurrentIndex(0)
        mw = QScrollArea()
        mw.setWidget(menu)
        self.layout.addWidget(mw)
        self.layout.addWidget(pl)
        self.setLayout(self.layout)
        self.setFixedSize(self.width, self.height)


class PlanetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        pass
