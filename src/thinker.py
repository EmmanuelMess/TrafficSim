class Thinker:
    def __init__(self):
        self.velocity = 0

    def viewDistance(self):
        return 20

    def step(self, deltaTime):
        self.velocity = 30

    def getVelocity(self):
        return self.velocity