from utils import toPairI, vec


class Polygon:
    def __init__(self, pointList, position=vec(0, 0), angle=0):
        self.pointList = pointList
        self.position = position
        self.angle = angle

    def move_ip(self, x, y):
        self.position = vec(x, y)

    def rotate_ip(self, angle):
        self.angle = angle

    def move(self, vector):
        return Polygon(self.pointList, vector, self.angle)

    def getPrintable(self):
        return [toPairI(point.rotate(self.angle) + self.position) for point in self.pointList]


    def __iter__(self):
        return (point for point in self.pointList)