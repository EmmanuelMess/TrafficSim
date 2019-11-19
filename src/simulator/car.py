import random

from simulator.trafficlights import RED


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