from pygame import Vector2

from simulator.car import Car
from simulator.map import Map
from simulator.source import SourceNode
from simulator.street import Street
from simulator.thinkers import thinker
from utils import dist_to_point


class Simulator:
    def __init__(self, intersections, adjacencyMatrix, trafficLightsByIntersectionId, sourceNodesRaw):
        streets = []
        streetIdsByIntersectionId = {}

        for (i, adjacents) in enumerate(adjacencyMatrix):
            for adjacent in adjacents:
                streets.append(Street(intersections[i], i, intersections[adjacent], adjacent, 20, 1))
                if i not in streetIdsByIntersectionId.keys():
                    streetIdsByIntersectionId[i] = []
                streetIdsByIntersectionId[i].append(len(streets)-1)

        sourceNodes = [SourceNode(pos, probability, streetId, self) for (pos, probability, streetId) in sourceNodesRaw]

        self.cars = []
        self.map = Map(streets, intersections, streetIdsByIntersectionId, trafficLightsByIntersectionId, sourceNodes)

    def createCar(self, thinkerCtor, streetId):
        self.cars.append(Car(self, thinkerCtor, streetId, self.map.streets[streetId].start, self.map))

    def createCarInPosition(self, thinker, streetId, position):
        self.cars.append(Car(self, thinker, streetId, position, self.map))

    def step(self, deltaTime):
        for car in self.cars:
            car.step(deltaTime)

        for trafficLight in self.map.trafficLightsByIntersectionId.values():
            trafficLight.step(deltaTime)

        for sourceNode in self.map.sourceNodes:
            sourceNode.step(deltaTime)

    def getCarRects(self):
        for car in self.cars:
            yield car.rect

    def getBundleForCar(self, car, streetId):
        street = self.map.streets[streetId]

        distanceToLaneEndLeft = min(dist_to_point(street.topLeft, street.topRight, Vector2(car.rect.topleft)),
                                    dist_to_point(street.topLeft, street.topRight, Vector2(car.rect.topright)),
                                    dist_to_point(street.topLeft, street.topRight, Vector2(car.rect.bottomleft)),
                                    dist_to_point(street.topLeft, street.topRight, Vector2(car.rect.bottomright)))

        distanceToLaneEndRight = min(dist_to_point(street.bottomLeft, street.bottomRight, Vector2(car.rect.topleft)),
                                     dist_to_point(street.bottomLeft, street.bottomRight, Vector2(car.rect.topright)),
                                     dist_to_point(street.bottomLeft, street.bottomRight, Vector2(car.rect.bottomleft)),
                                     dist_to_point(street.bottomLeft, street.bottomRight, Vector2(car.rect.bottomright)))

        return thinker.AmbientDataBundle(street.directionVector, street.upDirectionVector, street.downDirectionVector, distanceToLaneEndLeft, distanceToLaneEndRight)
