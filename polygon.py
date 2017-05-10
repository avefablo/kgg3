from bresenhammer import bresenham_line
from data_types import Segment, Point
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
        i = 0
        for e in sorted(v.output, key=lambda e: e.points[0].x):

            p1 = Point(round(e.points[0].x), round(e.points[0].y))
            p2 = Point(round(e.points[1].x), round(e.points[1].y))
            if self.check_point_inside_polygon(p1) and \
               self.check_point_inside_polygon(p2) and\
               not self.check_point_on_edge(p1) and \
               not self.check_point_on_edge(p2):
                self.bbb.append(Segment(p1, p2))
                print("\t({} {}) ({} {})".format(int(e.points[0].x),
                                               int(e.points[0].y),
                                               int(e.points[1].x),
                                               int(e.points[1].y)))
            else:
                print("({} {}) ({} {})".format(int(e.points[0].x),
                                                 int(e.points[0].y),
                                                 int(e.points[1].x),
                                                 int(e.points[1].y)))

            i += 1
        print(len(self.bbb))

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
