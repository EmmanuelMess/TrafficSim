import utils
from utils import vec, bigFast

class AmbientDataBundle:
    def __init__(self, streetDirectionVector, leftDirectionVector, rightDirectionVector, distanceToLaneEndLeft, distanceToLaneEndRight):
        self.streetDirectionVectors = (streetDirectionVector, leftDirectionVector, rightDirectionVector)
        self.distanceToLaneEndLeft = distanceToLaneEndLeft
        self.distanceToLaneEndRight = distanceToLaneEndLeft


MEDIAN_VELOCITY = 30
VISION_DISTANCE = 20

class Thinker:
    def __init__(self, getDataBundle):
        self.getDataBundle = getDataBundle
        self.medianVelocity = MEDIAN_VELOCITY
        self.velocity = vec(MEDIAN_VELOCITY, 0)
        self.visionDistance = VISION_DISTANCE

    def step(self, deltaTime):
        bundle = self.getDataBundle()
        (streetDirectionVector, leftDirectionVector, rightDirectionVector) = bundle.streetDirectionVectors

        self.velocity = utils.scale(streetDirectionVector, self.medianVelocity)

    def getVelocity(self):
        return self.velocity