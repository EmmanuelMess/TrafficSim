from polygon import Polygon
from utils import vec

CAR_POLYGON = Polygon([vec(-10, 5), vec(10, 5), vec(10, -5), vec(-10, -5)])

class Car:
    def __init__(self, simulator, thinker, streetId, position, map):
        self.thinker = thinker((lambda: simulator.getBundleForCar(self, streetId)))
        self.position = position
        self.map = map
        self.streetId = streetId
        self.direction = self.map.streets[self.streetId].getDefaultVector()

        self.polygon = CAR_POLYGON.move(position)

    def step(self, timeDelta):
        self.thinker.step(timeDelta)
        oldPos = self.position
        self.position = self.position + self.thinker.getVelocity() * timeDelta

        difPos = self.position - oldPos

        self.polygon.move_ip(self.position.x, self.position.y)
        self.polygon.rotate_ip(vec(1, 0).angle_to(self.thinker.getVelocity()))