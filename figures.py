from math import sqrt
from numpy import linalg as la
import numpy as np


class Polygon:
    def __init__(self, points, check=True):
        self.points = points
        if check and not (self.check_convex() and
                              self.check_self_intersection() and
                              self.check_num_of_edges()):
            raise ValueError('Not convex')

    def yield_edges(self):
        for i in range(len(self.points) - 1):
            yield (self.points[i], self.points[i + 1])
        yield (self.points[len(self.points) - 1], self.points[0])

    def check_num_of_edges(self):
        return len([x for x in self.yield_edges()]) == len(self.points)

    def check_convex(self):
        pos = False
        neg = False
        for i in range(len(self.points)):
            prev_, next_ = (i - 1) % len(self.points), \
                           (i + 1) % len(self.points)
            mv = self.mul_vecs(prev_, i, next_)
            pos = pos or mv > 0
            neg = neg or mv < 0
            if pos and neg:
                return False
        return True

    def check_self_intersection(self):
        for e1 in self.yield_edges():
            for e2 in self.yield_edges():
                if Segment(*e1).intersection(Segment(*e2)):
                    return False
        return True

    def mul_vecs(self, prev_, cur_, next_):
        dx1 = self.points[cur_][0] - self.points[prev_][0]
        dy1 = self.points[cur_][1] - self.points[prev_][1]
        dx2 = self.points[next_][0] - self.points[cur_][0]
        dy2 = self.points[next_][1] - self.points[cur_][1]
        return dx1 * dy2 - dy1 * dx2


class Circle:
    def __init__(self, c, r):
        self.center = c
        self.radius = r


class Segment:
    def __init__(self, p1, p2):
        self.A = p1[1] - p2[1]
        self.B = p2[0] - p1[0]
        self.C = p1[1] * p2[0] - p1[0] * p2[1]
        self.points = p1, p2

    def get_middle_point(self):
        return (self.points[0][0] + self.points[1][0]) // 2, \
               (self.points[0][1] + self.points[1][1]) // 2

    def get_orto_segm(self, y):
        middle = self.get_middle_point()
        s = Segment((0, 0), (0, 0))
        s.A = -self.B
        s.B = self.A
        s.C = -self.A * middle[1] + self.B * middle[0]
        s.reinit(y)
        return s

    def get_x(self, y):
        return int((-self.C - self.B * y) / self.A)

    def get_y(self, x):
        return int((-self.C - self.A * x) / self.B)

    def reinit(self, y):
        self.points = (0, self.get_y(0)), (self.get_x(y), y)

    def common_point(self, other):
        for p1 in self.points:
            for p2 in other.points:
                if p1 == p2:
                    return p1
        return None

    def intersection(self, other):
        d = self.A * other.B - self.B * other.A
        dx = self.C * other.B - self.B * other.C
        dy = self.A * other.C - self.C * other.A
        if d != 0:
            x = dx / d
            y = dy / d
            cp = self.common_point(other)
            return self.check_point_inside_segment((x, y)) and \
                   other.check_point_inside_segment((x, y)) and (x, y) != cp
        else:
            return False

    def check_point_inside_segment(self, p):
        ap = self.get_distance(self.points[0], p)
        bp = self.get_distance(p, self.points[1])
        ab = self.get_distance(self.points[0], self.points[1])
        return abs(ap + bp - ab) < 10e-8

    @staticmethod
    def get_distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


s = Segment((0, 0), (0, 0))
s.A = 4
s.B = -9
s.C = 3
p = s.get_orto_segm(800)
print(p.A, p.B, p.C)
