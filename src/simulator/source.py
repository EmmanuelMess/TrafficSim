from thinker import Thinker
from utils import shortest_dist_to_point


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

            self.simulator.createCarInPosition(Thinker(), self.streetId, shortest_dist_to_point(street.start, street.end, self.position))