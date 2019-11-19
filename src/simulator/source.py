from simulator.thinkers.thinker import Thinker
from utils import nearest_point_on_line


class SourceNode:
    def __init__(self, position, probability, streetId, simulator):
        self.position = position
        self.probability = probability
        self.streetId = streetId
        self.simulator = simulator

        self.time = 0

    def step(self, deltaTime):
        self.time += deltaTime

        if 1 <= self.time:
            self.time = 0

            street = self.simulator.map.streets[self.streetId]

            self.simulator.createCarInPosition(Thinker, self.streetId, nearest_point_on_line(street.start, street.end, self.position))