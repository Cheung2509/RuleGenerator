import random

from vgdl.ontology import BASEDIRS


class RandomController:
    def __init__(self, game):
        self.game = game


    def act(self, timer):
        possibleAction = self.game.getPossibleActions()
        action = random.choice(list(possibleAction.keys()))
        print(action)
        
        from vgdl.ontology import RIGHT, LEFT, UP, DOWN

        res = None
        if action == 'RIGHT':
            res = BASEDIRS.index(RIGHT)
        elif action == 'LEFT':
            res = BASEDIRS.index(LEFT)
        elif action == 'UP':
            res = BASEDIRS.index(UP)
        elif action == 'DOWN':
            res = BASEDIRS.index(DOWN)
        return res
