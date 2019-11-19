from math import hypot

from utils import vec, scale


class Street:
    def __init__(self, centerStart, startId, centerEnd, endId, width, lanes):
        self.start = centerStart
        self.startId = startId
        self.end = centerEnd
        self.endId = endId

        self.directionVector = centerEnd - centerStart
        self.length = centerStart.distance_to(centerEnd)
        self.width = width

        halfWidth = width/2

        self.upDirectionVector = self.directionVector.rotate(-90)
        self.downDirectionVector = self.directionVector.rotate(90)
        self.topLeft = centerStart + scale(self.upDirectionVector, halfWidth)
        self.topRight = centerEnd + scale(self.upDirectionVector, halfWidth)
        self.bottomRight = centerEnd + scale(self.downDirectionVector, halfWidth)
        self.bottomLeft = centerStart + scale(self.downDirectionVector, halfWidth)

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