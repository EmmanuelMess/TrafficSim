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