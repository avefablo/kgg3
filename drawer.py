from qtcarcas import Drawer
from PyQt4 import QtCore
from PyQt4 import QtGui
from data_types import Event


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
        qp.setPen(QtCore.Qt.green)
        for e in self.polygon.bbb:
            qp.drawLine(e.points[0].x, e.points[0].y,
                        e.points[1].x, e.points[1].y)
        qp.setPen(QtCore.Qt.blue)
        for circ in self.polygon.circles:
            qp.drawEllipse(QtCore.QPoint(circ.center.x, circ.center.y),
                            circ.radius, circ.radius)

    def draw_point(self, qp, p, color):
        qp.setPen(color)
        qp.drawPoint(p.x, p.y)
    
