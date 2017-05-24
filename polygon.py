import operator

from bresenhammer import bresenham_line
from data_types import Segment, Point, Circle
from misc import get_distance
from voronoi import Voronoi


class Polygon:
    def __init__(self, points, check=True):
        self.points = [Point(*x) for x in points]
        if len(self.points) < 3:
            raise ValueError('Not a polygon')
        self.edges = self.gen_edges()
        if check and not (
                        self.check_convex() and
                        self.check_self_intersection() and
                    self.check_num_of_edges()):
            raise ValueError('Not convex')
        self.bbb = []
        self.circles = None

    def voronoi(self):
        test = set()
        for e in self.edges:
            i = 0
            for u in bresenham_line(*e.points):
                if i % 20 == 0:
                    test.add(u)
                i += 1
        v = Voronoi(test)
        v.process()
        self.bbb = []
        voronoi_res = []
        ddd = {}
        for e in v.output:
            p01 = round(e.points[0].x), round(e.points[0].y)
            p02 = round(e.points[1].x), round(e.points[1].y)

            if p01 == p02:
                continue
            if p01 in ddd:
                ddd[p01] += 1
            else:
                ddd[p01] = 1
            p1 = Point(*p01)
            p2 = Point(*p02)
            voronoi_res.append(Segment(p1, p2))

        for e in voronoi_res:
            p1 = e.points[0]
            p2 = e.points[1]
            if self.check_point_inside_polygon(p1) and \
                    self.check_point_inside_polygon(p2) and \
                    not self.check_point_on_edge(p1) and \
                    not self.check_point_on_edge(p2):
                self.bbb.append(e)

        self.filter_bbb(voronoi_res, ddd)


    def filter_bbb(self, vor_out, ddd):
        filtered = []
        for e1 in sorted(self.bbb, key=lambda e: e.points[0].x):
            p11 = (e1.points[0].x, e1.points[0].y)
            p12 = e1.points[1]
            if ddd[p11] == 1:
                filtered.append(e1)
            else:
                for e2 in vor_out:
                    p21 = e2.points[0]
                    p22 = e2.points[1]
                    s = Segment(p12, p22)
                    if p21 == p11 \
                            and not s.check_point_inside_segment(p21):
                        filtered.append(e1)
        self.bbb = filtered

    def gen_circle(self, c1=None):
        p = set()
        for e in self.bbb:
            for y in bresenham_line(*e.points):
                p.add(y)
        max_rad = 0.0
        max_point = (0, 0)
        for point in p:
            min_that = min(x.distance_to_point(point) for x in self.edges)
            if c1 is None:
                if max_rad < min_that:
                    max_rad = min_that
                    max_point = point
            else:
                if max_rad < min_that \
                        and c1.radius + min_that <= get_distance(c1.center, point):
                    max_rad = min_that
                    max_point = point

        return Circle(max_point, max_rad)

    def gen_circles(self):
        c1 = self.gen_circle()
        c2 = self.gen_circle(c1=c1)
        return c1, c2

    def gen_edges(self):
        s = []
        for i in range(len(self.points) - 1):
            segm = Segment(self.points[i], self.points[i + 1])
            s.append(segm)
        segm = Segment(self.points[len(self.points) - 1], self.points[0])
        s.append(segm)
        return s

    def check_num_of_edges(self):
        return len(self.edges) == len(self.points)

    def check_convex(self):
        pos = False
        neg = False
        for i in range(len(self.points)):
            prev_ind, next_ind = (i - 1) % len(self.points), \
                                 (i + 1) % len(self.points)
            prev_, cur_, next_ = self.points[prev_ind], \
                                 self.points[i], \
                                 self.points[next_ind]
            mv = self.mul_vecs(prev_, cur_, next_)
            pos = pos or mv > 0
            neg = neg or mv < 0
            if pos and neg:
                return False
        return True

    def check_point_inside_polygon(self, p):
        pos = False
        neg = False
        for e in self.edges:
            mv = self.mul_vecs(*e.points, p)
            pos = pos or mv > 0
            neg = neg or mv < 0

            if pos and neg:
                return False
        return True

    def check_point_on_edge(self, p):
        for e in self.edges:
            if e.check_point_inside_segment(p, delta=1):
                return True
        return False

    def check_self_intersection(self):
        for e1 in self.edges:
            for e2 in self.edges:
                if e1.is_intersect(e2):
                    return False
        return True

    def mul_vecs(self, prev_, cur_, next_):
        dx1 = cur_.x - prev_.x
        dy1 = cur_.y - prev_.y
        dx2 = next_.x - cur_.x
        dy2 = next_.y - cur_.y
        return dx1 * dy2 - dy1 * dx2
