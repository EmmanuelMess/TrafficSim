class Intersection:
    def __init__(self, position, streets):
        self.polygon = []

        for street in streets:
            if position.distance_to(street.start) < position.distance_to(street.end):
                self.polygon.append(street.topLeft)
                self.polygon.append(street.bottomLeft)
            else:
                self.polygon.append(street.topRight)
                self.polygon.append(street.bottomRight)

    def getPolygon(self):
        return self.polygon