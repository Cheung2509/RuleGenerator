from RuleGenerationProject.vgdl.core import VGDLParser
from RuleGenerationProject.aiGame import aiGame
from RuleGenerationProject.MCTSPlayer import Agent
from RuleGenerationProject.Timer import ElapsedCPUTimer
import sys
import copy
import random

class Chromosome:
    def __init__(self, interaction, terminations, level):
        self.fitness = list
        self.constrainFitness = 0
        self.badFrames = 0
        self.errorCount = 0

        self.interaction = interaction
        self.terminations = terminations
        self.stepLimit = 40
        self.level = level

    def compareTo(self, o):
        if self.constrainFitness < 1 or o.constrainFitness < 1:
            if self.contrainFitness < o.constrainFitness:
                return 1

            if self.contrainFitness > o.constrainFitness:
                return -1

            return 0

        firstFitness = 0.0
        secontFitness = 0.0

        for fitness in self.fitness:
            firstFitness += fitness
            secontFitness += o.fitness[self.fitness.index(fitness)]

        if firstFitness > secontFitness:
            return -1
        elif firstFitness < secontFitness:
            return 1

        return 0

    def crossover(self, c):
        children = list()
        children.append(copy.deepcopy(self))
        children.append(copy.deepcopy(c))

        point1 = random.randint(0, len(self.interaction))
        point2 = random.randint(0,len(c.interaction))

        "Calculate the size of interaction set"
        size1 = point1 + (len(c.interaction) - point2)
        size2 = point2 + (len(self.interaction) - point1)

        interactionSet1 = list()
        interactionSet2 = list()

        "swap interactions 1"
        for i in range(0, point1):
            interactionSet1[i] = self.interaction[i]

        counter = point2
        for i in range(point1, size1):
            interactionSet1[i] = c.interaction[counter]
            counter += 1

        children[0].interaction = interactionSet1
        children[1].interaction = interactionSet2

        "Swap interaction 2"
        for i in range(0, point2):
            interactionSet2[i] = c.interaction[i]
        counter = point1
        for i in range(point2, size2):
            interactionSet2[i] = c.interaction[i]

        "Calculate termination set"
        point1 = random.randint(len(self.terminations))
        point2 = random.randint(len(c.terminactions))

        size1 = point1 + (len(c.terminactions) - point2)
        size2 = point2 + (len(self.terminations) - point1)

        terminationSet1 = list()
        terminationSet2 = list()

        for i in range(0, point1):
            terminationSet1[i] = self.terminations[i]
        counter = point2
        for i in range(point1, size1):
            terminationSet1[i] = c.terminactions[counter]
            counter += 1

        for i in range(0, point2):
            terminationSet2[i] = c.terminactions[i]
        counter = point1
        for i in range(point2, size2):
            terminationSet2[i] = c.terminactions[counter]

        c[0].terminations = terminationSet1
        c[1].terminations = terminationSet2

        return children

    def mutate(self):
        mutationCount = random.randint(0, 2)

        for i in range(0, mutationCount):
            'Flip a coin to determine to mutate interactions or terminations'
            mutateR = random.getrandbits(1)
            if mutateR is 1:
                self.mutateInteraction()
            else:
                self.mutateTermination()

    def mutateInteraction(self):
        'TODO: add mutation of interactions'

    def mutateTermination(self):
        'TODO: add mutation of terminations'


    def calculateFitness(self, time):

        self.badFrames = 0

        state = self.feasibilityTest()

        if self.constrainFitness < 0.7:
            self.fitness.insert(0, self.constrainFitness)
        else:
            score = -200
            winSum = 0.0
            frameCount = 0
            for r in range(0, 3):
                tempState = copy.copy(state)
                agent = Agent(self.game, time)
                temp = self.getAgentResult(tempState, 300, agent, False)
                frameCount += temp

                score = tempState.getScore()

                gameOver, win = tempState._isDone()
                if win:
                    winSum += 1
                else:
                    winSum == 0.5

        "TODO: Need to create event recorder to calculate unique interactions"

        "Apply fitness"
        fitness = (score + 1)
        constrainFitness = 1.0
        self.fitness.insert(0, constrainFitness)
        self.fitness.insert(1, fitness)

    def feasibilityTest(self):
        try:
            parser = VGDLParser()
            game = parser.parseGame(self.ruleSet)
            game.buildLevel(self.level)
            state = aiGame(game)
        except:
            self.errorCount += 1
            pass

        self.constrainFitness = 0
        self.constrainFitness += (0.5) * 1.0 / (self.errorCount + 1.0)


        if self.constrainFitness >= 0.5:
            doNothingLength = sys.maxsize
            temp = self.getAgentResult(self, copy.copy(state), 50, True)

            if temp < doNothingLength:
                doNothingLength = temp

        self.constrainFitness += 0.2 * (doNothingLength / 40.0)
        self.fitness.insert(0, self.constrainFitness)


        return aiGame

    def getAgentResult(self, state, steps, agent, doNothing=False):

        for a in range(0, 3):
            for i in range(0, steps):
                if state.isGameOver():
                    break
                timer = ElapsedCPUTimer()
                timer.setMaxTime(40)
                if doNothing:
                    action = agent.act(state, timer)
                    state.act(action)
                else:
                    state.act()

        return i