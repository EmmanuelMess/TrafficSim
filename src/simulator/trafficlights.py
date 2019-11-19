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