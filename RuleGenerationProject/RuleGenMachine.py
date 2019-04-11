import random
from vgdl.core import VGDLParser
from Time import ElapsedCPUTimer
import copy

class RuleGenMachine:
    staticmethod
    def generateRules(self, game, level, modifiedFile):
        parser = VGDLParser()
        game = parser.parseGame(game)

        generator = RuleGenerator()

    staticmethod
    def getGeneratedRules(self, generator, level):
        timer = ElapsedCPUTimer()
        timer.setMaxTimeMillis(1800000*10)

        rules = generator.generateRuleSet(copy.deepcopy( timer))

        if timer.elapsed().microseconds > 180000*10:
            exceeded = -timer.remainingTimeMillis()

        return rules
