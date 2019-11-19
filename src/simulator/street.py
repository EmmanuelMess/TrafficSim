from math import hypot

from utils import vec


class Street:
    def __init__(self, start, startId, end, endId):
        self.start = start
        self.startId = startId
        self.end = end
        self.endId = endId

        self.defaultVector = vec(self.end.x - self.start.x, self.end.y - self.start.y).normalize()

    def length(self):
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)

    def getDefaultVector(self):
        return self.defaultVector

    def getVector(self, currentDirectionVector):
        if self.defaultVector.angle_to(currentDirectionVector) < 90:
            return self.defaultVector
        else:
            return self.defaultVector.rotate(180)

    def getIntersection(self, currentDirectionVector):
        if self.defaultVector.angle_to(currentDirectionVector) < 90:
            return self.end
        else:
            return self.start

    def getIntersectionId(self, currentDirectionVector):
        if self.defaultVector.angle_to(currentDirectionVector) < 90:
            return self.endId
        else:
            return self.startId