from MCTSPlayer.MCTSNode import MCTSNode
import copy


class Player:
    def __init__(self, numOfActions, actions):
        self.numOfActions = numOfActions
        self.actions = actions
        self.rootNode = MCTSNode(numOfActions, actions, None)

    def init(self, state):
        self.rootNode = MCTSNode(self.numOfActions, self.actions, None)
        self.rootNode.rootState = state

    def run(self, timer, obs):
        self.rootNode.search(timer, obs)

        action = self.rootNode.mostVisitedAction()
        return action
