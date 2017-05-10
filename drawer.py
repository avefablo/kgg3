from data_types import Segment
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
        qp.setPen(QtCore.Qt.red)
        for e in self.polygon.edges:
            qp.drawLine(e.points[0].x, e.points[0].y,
                        e.points[1].x, e.points[1].y)
        qp.setPen(QtCore.Qt.blue)
        for e in self.polygon.bbb:

            qp.drawLine(e.points[0].x, e.points[0].y,
                        e.points[1].x, e.points[1].y)

    def draw_point(self, qp, p, color):
        qp.setPen(color)
        qp.drawPoint(p.x, p.y)
