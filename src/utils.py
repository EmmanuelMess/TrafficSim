from pygame.math import Vector2


def vec(x, y):
    v = Vector2()
    v.xy = x, y
    return v


def scale(v, l):
    v.scale_to_length(l)
    return v


def toPairI(vec):
    return (int(vec.x), int(vec.y))


def dist_to_point(start, end, other_point):
    dx = end.x - start.x
    dy = end.y - start.y
    dr2 = float(dx *dx + dy * dy)

    lerp = ((other_point.x - start.x) * dx + (other_point.y - start.y) * dy) / dr2
    if lerp < 0:
        lerp = 0
    elif lerp > 1:
        lerp = 1

    x = lerp * dx + start.x
    y = lerp * dy + start.y

    return vec(x, y).distance_to(other_point)


def nearest_point_on_line(start, end, other_point):
    dx = end.x - start.x
    dy = end.y - start.y
    dr2 = float(dx *dx + dy * dy)

    lerp = ((other_point.x - start.x) * dx + (other_point.y - start.y) * dy) / dr2
    if lerp < 0:
        lerp = 0
    elif lerp > 1:
        lerp = 1

    x = lerp * dx + start.x
    y = lerp * dy + start.y

    return vec(x, y)

#TODO fix
def bigFast(t, valueOn0):
    return -abs(t)+valueOn0