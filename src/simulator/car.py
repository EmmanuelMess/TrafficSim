import random

from pygame.rect import Rect

from simulator import simulator
from simulator.trafficlights import RED

CAR_RECT = Rect(0, 0, 20, 10)

class Car:
    def __init__(self, simulator, thinker, streetId, position, map):
        self.thinker = thinker((lambda: simulator.getBundleForCar(self, streetId)))
        self.position = position
        self.map = map
        self.streetId = streetId
        self.direction = self.map.streets[self.streetId].getDefaultVector()

        self.rect = CAR_RECT.copy()
        self.rect.center = position.x, position.y

    def step(self, timeDelta):
        self.thinker.step(timeDelta)
        self.position = self.position + self.thinker.getVelocity() * timeDelta

        self.rect.center = self.position.x, self.position.y