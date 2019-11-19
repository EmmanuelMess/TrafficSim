from simulator.car import Car
from simulator.map import Map
from simulator.source import SourceNode
from simulator.street import Street


class Simulator:
    def __init__(self, intersections, adjacencyMatrix, trafficLightsByIntersectionId, sourceNodesRaw):
        streets = []
        streetIdsByIntersectionId = {}

        for (i, adjacents) in enumerate(adjacencyMatrix):
            for adjacent in adjacents:
                streets.append(Street(intersections[i], i, intersections[adjacent], adjacent))
                if i not in streetIdsByIntersectionId.keys():
                    streetIdsByIntersectionId[i] = []
                streetIdsByIntersectionId[i].append(len(streets)-1)

        sourceNodes = [SourceNode(pos, probability, streetId, self) for (pos, probability, streetId) in sourceNodesRaw]

        self.cars = []
        self.map = Map(streets, intersections, streetIdsByIntersectionId, trafficLightsByIntersectionId, sourceNodes)

    def createCar(self, thinker, streetId):
        self.cars.append(Car(thinker, streetId, self.map.streets[streetId].start, self.map))

    def createCarInPosition(self, thinker, streetId, position):
        self.cars.append(Car(thinker, streetId, position, self.map))

    def step(self, deltaTime):
        for car in self.cars:
            car.step(deltaTime)

        for trafficLight in self.map.trafficLightsByIntersectionId.values():
            trafficLight.step(deltaTime)

        for sourceNode in self.map.sourceNodes:
            sourceNode.step(deltaTime)

    def getCarPositions(self):
        for car in self.cars:
            yield car.pos

