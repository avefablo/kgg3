#!/usr/bin/python3


from PyQt4 import QtGui
import sys
from drawer import VoronoiDrawer
from qtcarcas import Carcass
from polygon import Polygon
from random import randint


def main():
    app = QtGui.QApplication(sys.argv)
    poly = Polygon(random_poly(length=6),
                   #[(100, 100), (500, 100), (500, 200), (100, 300)],
                   check=True)
    poly.voronoi()
    poly.circles = poly.gen_circles()
    ex = Carcass(VoronoiDrawer(poly))
    app.exec_()
    app.deleteLater()
    exit()


def random_poly(convex=True, length=6):
    while True:
        p = []
        for i in range(length):
            p.append((randint(0, 1000), randint(0, 600)))

        if not convex:
            return p
        else:
            t = Polygon(p, check=False)
            if t.check_convex() and t.check_self_intersection():
                print(p)
                return p

if __name__ == '__main__':
    main()
