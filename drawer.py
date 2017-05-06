from figures import Segment
from qtcarcas import Drawer
from math import sqrt, sin, cos, tan
from PyQt4 import QtCore
from bresenhammer import bresenham_line


class VoronoiDrawer(Drawer):
    def __init__(self, polygon):
        super().__init__()
        self.size = None
        self.polygon = polygon

    def draw(self, qp):
        self.draw_polygon(qp)

    def draw_polygon(self, qp):
        poly = self.polygon
        for e in poly.yield_edges():
            for p in bresenham_line(e[0], e[1]):
                self.draw_point(qp, p, QtCore.Qt.red)
            orto = Segment(*e).get_orto_segm(self.size.height())
            print(orto.points)
            for p in bresenham_line(orto.points[0], orto.points[1]):
                self.draw_point(qp, p, QtCore.Qt.blue)

    def draw_point(self, qp, p, color):
        qp.setPen(color)
        qp.drawPoint(p[0], p[1])
