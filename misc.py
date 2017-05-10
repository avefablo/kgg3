from math import sqrt


def get_distance(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
