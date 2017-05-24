import heapq
import itertools

from misc import get_distance


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Arc:
    def __init__(self, p, a=None, b=None):
        self.p = p
        self.pprev = a
        self.pnext = b
        self.e = None
        self.s0 = None
        self.s1 = None


class Circle:
    def __init__(self, c, r):
        self.center = c
        self.radius = r


class Segment:
    def __init__(self, p1, p2):
        self.points = p1, p2
        self.orto = None
        self.A = None
        self.B = None
        self.C = None
        if p2 is not None:
            self.init_coeffs()

    def finish(self, p):
        if self.points[1] is None:
            self.points = self.points[0], p
        self.init_coeffs()

    def init_coeffs(self):
        p1, p2 = self.points
        self.A = p1.y - p2.y
        self.B = p2.x - p1.x
        self.C = p1.y * p2.x - p1.x * p2.y

    def common_point(self, other):
        for p1 in self.points:
            for p2 in other.points:
                if p1 == p2:
                    return p1
        return None

    def is_intersect(self, other):
        d = self.A * other.B - self.B * other.A
        dx = self.C * other.B - self.B * other.C
        dy = self.A * other.C - self.C * other.A
        if d != 0:
            x = dx / d
            y = dy / d
            cp = self.common_point(other)
            p = Point(x, y)

            return self.check_point_inside_segment(p) and \
                   other.check_point_inside_segment(p) and p != cp
        else:
            return False

    def check_point_inside_segment(self, p, delta=10e-8):
        ap = get_distance(self.points[0], p)
        bp = get_distance(p, self.points[1])
        ab = get_distance(self.points[0], self.points[1])
        return abs(ap + bp - ab) < delta

    def this_len(self):
        return get_distance(self.points[0], self.points[1])

    def distance_to_point(self, p):
        return abs(self.A*p.x+self.B*p.y-self.C)/self.this_len()

class Event:
    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True


class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def push(self, item):
        if item in self.entry_finder:
            return
        count = next(self.counter)
        # use x-coordinate as a primary key (heapq in python is min-heap)
        entry = [item.x, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove_entry(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = 'Removed'

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def empty(self):
        return not self.pq
