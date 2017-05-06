#!/usr/bin/python3


from PyQt4 import QtGui
import sys
from drawer import VoronoiDrawer
from qtcarcas import Carcass
from math import cos, sin
from solver import Solver
from figures import Polygon, Circle
from random import randint


def main():
    app = QtGui.QApplication(sys.argv)
    poly = Polygon(random_poly(length=6), check=True)
    ex = Carcass(VoronoiDrawer(poly))
    app.exec_()
    app.deleteLater()
    exit()


def random_poly(convex=True, length=5):
    while True:
        p = []
        for i in range(length):
            p.append((randint(0, 1000), randint(0, 600)))
        if not convex:
            return p
        else:
            t = Polygon(p, check=False)
            if t.check_convex() and t.check_self_intersection():
                return p

if __name__ == '__main__':
    main()
