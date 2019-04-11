from RuleGenerationProject.RandomRuleGenerator import RandomRuleGenerator
from Chromosome import Chromosome
from RuleGenerationProject.Timer import ElapsedCPUTimer
import random
import copy

class RuleGenerator:
    def __init__(self):
        self.bestFitness = list()
        self.numOfFeasible = list()
        self.numOfInFeasible = list()
        self.chromosomes = list()

    def generateRuleset(self, time, game, level):

        fChromosomes = list()
        iChromosomes = list()
        allChromosomes = list()

        allChromosomes = self.getFirstPopulation(game, level, 50, 0, time)

        worstTime = 4 * 10000 * 50
        averageTime = worstTime
        totalTime = 0
        numberOfLoops = 0

        while time.remainingMillis() > 4 * averageTime and time.remainingMillis() > worstTime:
            timer = ElapsedCPUTimer()
            fChromosomes.clear()
            iChromosomes.clear()

            for c in allChromosomes:
                if c.constrainFitness < 1:
                    'Discard unfit chromosomes'
                    iChromosomes.append(c)
                else:
                    'Keep fit chromosoms'
                    fChromosomes.append(c)

                chromosomes = self.getNextPopulation(fChromosomes, iChromosomes)
                numberOfLoops += 1
                totalTime = timer.elapsed().microseconds
                averageTime = totalTime / numberOfLoops


        'if there are no feasible chomosomes get best chromosome in infeasible'
        if fChromosomes.count() == 0:
            bestFitness = 0
            index = 0
            for c in iChromosomes:
                timer = ElapsedCPUTimer()
                timer.setMaxTime(40)
                c.calculateFitness(timer)

                if bestFitness < c.fitness:
                    bestFitness = c.fitness
                    index = iChromosomes.index(c)

            return iChromosomes[index]
        else:
            for c in fChromosomes:
                timer = ElapsedCPUTimer()
                timer.setMaxTime(40)
                c.calculateFitness(timer)
                if bestFitness < c.fitness:
                    bestFitness = c.fitness
                    index = fChromosomes.index(c)


        return fChromosomes[index].interaction, fChromosomes[index].terminations

    def getFirstPopulation(self, game, level, amount, mutations, timer):
        generator = RandomRuleGenerator(level, game, timer)
        chromosomes = list()

        'Create initial population'
        for i in range(0, amount):
            interactions, terminations = generator.generateRuleSet(timer)
            c = Chromosome(interactions, terminations)
            c.calculateFitness(1000)

            for j in range(0, mutations):
                c.mutate

            chromosomes.append(c)

        return chromosomes

    def getNextPopulation(self, fPopulation, iPopulation):
        newPopulation = list()

        fitness = list()

        for i in fPopulation:
            fitness.append(i.fitness[0])

        self.numOfFeasible.append(fPopulation.count())
        self.numOfInFeasible.append(iPopulation.cout())

        'Generate new population'
        while newPopulation.count() < 50:
            population = fPopulation
            if fPopulation.count() <= 0:
                population = iPopulation
            if random.random() < 0.5:
                population = iPopulation
                if iPopulation.count() <= 0:
                    population = fPopulation

            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child1 = copy.deepcopy(parent1)
            child2 = copy.deepcopy(parent2)

            'Roll a dice to check if crossover is needed'
            if random.random() < 0.9:
                children = list()
                children.append(parent1.crossover(parent2))
                child1 = children[0]
                child2 = children[1]

                'Roll a dice to check if mutation is needed'
                if random.random() < 0.1:
                    child1.mutate()

                if random.random() < 0.1:
                    child2.mutate()
            newPopulation.append(child1)
            newPopulation.append(child2)

        for c in newPopulation:
            timer = ElapsedCPUTimer()
            timer.setMaxTime(40)
            c.calculateFitness(timer)

        return newPopulation



