from MCTSPlayer.Player import Player
from vgdl.ontology import BASEDIRS


class Agent:

    def __init__(self, game, timer):
        self.game = game
        self.actions = game.getPossibleActions()
        self.numberOfActions = len(self.actions)

        self.Player = Player(self.numberOfActions, self.actions)

    def act(self, obs, timer):
        self.Player.init(obs)
        action = self.Player.run(timer, obs)
        print(action)

