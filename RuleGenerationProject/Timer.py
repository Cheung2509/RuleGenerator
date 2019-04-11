from datetime import datetime


class ElapsedCPUTimer:

    def __init__(self):
        self.start = datetime.now()
        self.maxTimer = 0

    def setMaxTime(self, maxTime):
        self.maxTimer = maxTime

    def remainingTimeMillis(self):
        diff = self.maxTimer - self.elapsed().microseconds
        return diff

    def elapsed(self):
        return datetime.now() - self.start