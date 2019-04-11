import copy
import random
import sys

import math


class MCTSNode:
    ROLLOUT_DEPTH = 10
    rootState = None

    def normalise(a, b, c):
        if b < c:
            return (a - b) / (c - b)
        else:
            return a

    @staticmethod
    def noise(input, epsilon, rand):
        if input != -epsilon:
            return (input + epsilon) * (1.0 + epsilon * (rand - 0.5))
        else:
            return (input + epsilon) * (1.0 + epsilon * (rand - 0.5))

    def __init__(self, numOfActions, actions, parent, index=-1, child=False):
        if child:
            self.initailizeChild(parent, index, numOfActions, actions)
        else:
            self.numOfActions = numOfActions
            self.parent = None
            self.actions = actions
            self.childIndex = index
            self.depth = 0

        self.epsilon = 1e-6
        self.eGreedyEpsilon = 0.05
        self.totalValue = 0
        self.numberOfVisits = 0
        self.bounds = [sys.float_info.max, -sys.float_info.max]
        self.rollOutDepth = 10
        self.k = math.sqrt(2)
        self.children = [None] * numOfActions

    def initailizeChild(self, parent, childIndex, numOfActions, actions):
        self.parent = parent
        self.numOfActions = numOfActions
        self.actions = actions
        self.childIndex = childIndex
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def search(self, elapsedTime, obs):
        avgTime = 0
        acumTime = 0
        timeRemaining = elapsedTime.remainingTimeMillis()
        numIters = 0

        remainLimit = 5

        while timeRemaining > 2 * avgTime and timeRemaining > remainLimit:
            state = copy.copy(self.rootState)

            nodeSelected = self.treePolicy(state)
            delta = nodeSelected.rollOut(state)

            numIters += 1
            acumTime += elapsedTime.elapsed().microseconds
            avgTime = acumTime / numIters
            timeRemaining = elapsedTime.remainingTimeMillis()

    def treePolicy(self, state):
        cur = self

        while not state.isGameOver() and cur.depth < self.ROLLOUT_DEPTH:
            if cur.notFullyExpanded():
                return cur.expand(state)
            else:
                next = cur.uct(state)
                cur = next

        return cur

    def expand(self, state):
        bestAction = 0
        bestValue = -1

        for i in self.children:
            x = random.random()
            if x > bestValue and i == None:
                bestAction = self.children.index(i)
                bestValue = x

        action = list(self.actions.keys())[bestAction]
        state.performAction(bestAction)

        treeNode = MCTSNode(self.numOfActions, self.actions, self, bestAction, True)
        self.children[bestAction] = treeNode

        return treeNode

    def uct(self, state):
        selectedNode = None
        bestValue = -sys.float_info.max

        for x in self.children:
            hvVal = x.totalValue
            childValue = hvVal / (x.numberOfVisits + self.epsilon)

            childValue = MCTSNode.normalise(childValue, self.bounds[0], self.bounds[1])

            uctValue = childValue + self.k * math.sqrt(
                math.log(self.numberOfVisits + 1) / (x.numberOfVisits + self.epsilon))

            uctValue = MCTSNode.noise(uctValue, self.epsilon, random.random())

            if uctValue > bestValue:
                selectedNode = x
                bestValue = uctValue

        if selectedNode == None:
            print("Error")
            # throw Exception here

        state.performAction(selectedNode.childIndex)

        return selectedNode

    def rollOut(self, state):
        depth = self.depth

        while not self.finishRollout(state, depth):
            temp = random.choice(list(self.actions))
            action = list(self.actions.keys()).index(temp)
            state.performAction(action)
            depth += 1

        delta = self.value(state)

        if delta < self.bounds[0]:
            self.bounds[0] = delta
        if delta > self.bounds[1]:
            self.bounds[1] = delta

        return delta

    def finishRollout(self, rollerState, depth):
        if depth >= self.rollOutDepth:
            return True

        if rollerState.isGameOver():
            return True

        return False

    def calcValue(self, state):
        gameOver = state.isGameOver()
        win = state.getWinner()
        rawScore = state.getScore()

        if gameOver == True and win == False:
            rawScore += -10000000.0
            print('Lost!!')

        if gameOver == True and win == True:
            rawScore += 10000000.0
            print('won!!')

        return rawScore

    def backUp(self, node, result):
        n = node

        while n != None:
            ++n.numberOfVisits
            n.totalValue += result
            if result < n.bounds[0]:
                n.bounds[0] = result

            if result < n.bounds[1]:
                n.bounds[1] = result

            n = n.parent

    def mostVisitedAction(self):
        selected = -1
        bestValue = -sys.float_info.max
        allEqual = True
        first = -1

        for child in self.children:
            if (child != None):
                if (first == -1):
                    first = child.numberOfVisits
                elif first != child.numberOfVisits:
                    allEqual = False

                childValue = child.numberOfVisits
                childValue = self.noise(childValue, self.epsilon, random.random())

                if childValue > bestValue:
                    bestValue = childValue
                    selected = self.children.index(child)

        if selected == -1:
            print("No Selection!")
            selected = 0
        elif allEqual:
            selected = self.bestAction()

        return selected

    def bestAction(self):
        selected = -1
        bestValue = -sys.float_info.max

        for child in self.children:
            if (child != None):
                childValue = child.totalValue / (child.numberOfVisits + self.epsilon)
                childValue = MCTSNode.noise(childValue, self.epsilon, random.random())

                if childValue > bestValue:
                    bestValue = childValue
                    selected = child.childIndex

        if selected == -1:
            print("No Selection!")
            selected = 0

        return selected

    def notFullyExpanded(self):
        for child in self.children:
            if child == None:
                return True

        return False

    def value(self, state):
        gameOver, win = state._isDone()
        rawScore = state.getScore()

        if gameOver and win:
            rawScore += 10000000.0
            print('Win!!')


        if gameOver and not win:
            rawScore += 10000000.0
            print('Lost!!')

        return rawScore
