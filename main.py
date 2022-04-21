from math import sin, cos, pi

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getCoord(self):
        return self.x, self.y, self.z


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)


def getPoint(v, u) -> Point:
    x = sin(pi * v) * cos(2 * pi * u)
    y = sin(pi * v) * sin(2 * pi * u)
    z = cos(pi * v)
    return Point(x, y, z)


edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

uStepsNum = 50
vStepsNum = 50


def Sphere():
    glBegin(GL_LINE_LOOP)
    quadObj = gluNewQuadric()
    glPushMatrix()
    glColor3d(1, 0, 0)
    gluQuadricDrawStyle(quadObj, GLU_LINE)
    gluSphere(quadObj, 1, 100, 100)


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(0.1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Sphere()
        pygame.display.flip()
        pygame.time.wait(10)


main()
