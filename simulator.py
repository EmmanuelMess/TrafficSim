import random
from math import hypot

from thinker import Thinker
from utils import vec, shortest_dist_to_point


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


class Map:
    def __init__(self, streets, intersections, streetIdsByIntersectionId, trafficLightsByIntersectionId, sourceNodes):
        self.streets = streets
        self.intersections = intersections
        self.streetIdsByIntersectionId = streetIdsByIntersectionId
        self.trafficLightsByIntersectionId = trafficLightsByIntersectionId
        self.sourceNodes = sourceNodes

    def getStreetById(self, streetId):
        return self.streets[streetId]

    def getTrafficLightById(self, intersectionId):
        if intersectionId in self.trafficLightsByIntersectionId.keys():
            return self.trafficLightsByIntersectionId[intersectionId]
        else:
            return None

    def getNextIds(self, intersectionId):
        if intersectionId in self.streetIdsByIntersectionId.keys():
            return self.streetIdsByIntersectionId[intersectionId]
        else:
            return []


RED = 0
YELLOW = 1
GREEN = 2

class TrafficLight:
    def __init__(self, timingRed, timingYellow, timingGreen):
        self.timingRed = timingRed
        self.timingYellow = timingYellow
        self.timingGreen = timingGreen
        self.time = 0

    def getState(self):
        if self.time <= self.timingRed:
            return RED
        elif self.time <= self.timingRed + self.timingYellow:
            return YELLOW
        elif self.time <= self.timingRed + self.timingYellow + self.timingGreen:
            return GREEN
        else:
            return YELLOW

    def step(self, deltaTime):
        self.time = (self.time + deltaTime) % (self.timingRed + self.timingYellow * 2 + self.timingGreen)


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


class Car:
    def __init__(self, thinker, streetId, pos, map):
        self.thinker = thinker
        self.pos = pos
        self.map = map
        self.streetId = streetId
        self.direction = self.map.streets[self.streetId].getDefaultVector()

    def step(self, deltaTime):
        self.thinker.step(deltaTime)

        movementVector = self.map.streets[self.streetId].getVector(self.direction)
        movementVector.scale_to_length(deltaTime*self.thinker.getVelocity())

        nextIntersectionCenter = self.map.streets[self.streetId].getIntersection(movementVector)

        if movementVector.length() < self.pos.distance_to(nextIntersectionCenter):
            self.pos = self.pos + movementVector
        else:
            nextIntersectionId = self.map.streets[self.streetId].getIntersectionId(movementVector)
            nextIds = self.map.getNextIds(nextIntersectionId)

            nextIntersectionTrafficLight = self.map.getTrafficLightById(nextIntersectionId)
            if nextIntersectionTrafficLight is not None and nextIntersectionTrafficLight.getState() == RED:
                self.pos = self.pos
            elif not nextIds:
                self.pos = nextIntersectionCenter
            else:
                movementDistance = movementVector.length()
                movementDistance -= self.pos.distance_to(nextIntersectionCenter)

                nextStreetId = random.choice(self.map.getNextIds(nextIntersectionId))
                nextStreet = self.map.streets[nextStreetId]

                self.streetId = nextStreetId
                self.direction = (nextStreet.getDefaultVector()) if (nextStreet.startId == nextIntersectionId) else nextStreet.getDefaultVector().rotate(180)

                streetVector = self.direction
                streetVector.scale_to_length(movementDistance)
                self.pos = nextStreet.start + streetVector
