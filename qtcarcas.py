import sys, random
from PyQt4 import QtGui, QtCore


class Carcass(QtGui.QGraphicsView):
    def __init__(self, drawer):
        super(Carcass, self).__init__()
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.drawer = drawer
        self.init_ui()
        self.drawer.size = self.size()
        self.draw_pic()

    def init_ui(self):
        self.setGeometry(0, 0, 1200, 700)
        self.setWindowTitle('Voronoi')
        self.show()


    def draw_pic(self):
        self.drawer.size = self.size()
        pix = QtGui.QPixmap(QtCore.QSize(self.size().width(), self.size().height()))
        pix.fill(QtCore.Qt.white)
        qp = QtGui.QPainter(pix)
        self.drawer.draw(qp)
        qp.end()
        self.scene.addPixmap(pix)


class Drawer:
    def __init__(self):
        pass

    def draw(self, qp):
        pass
