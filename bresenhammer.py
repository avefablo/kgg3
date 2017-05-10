from data_types import Point
def bresenham_line(p1, p2):
    x0 = p1.x
    x1 = p2.x
    y0 = p1.y
    y1 = p2.y

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield Point(x0 + x * xx + y * yx, y0 + x * xy + y * yy)
        if D > 0:
            y += 1
            D -= dx
        D += dy
