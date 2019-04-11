import pygame
from vgdl.interfaces import GameEnvironment
from vgdl.ontology import BASEDIRS
from vgdl.subjective import SubjectiveSceen
from Timer import ElapsedCPUTimer

blocky = ['wall']

class aiGame(GameEnvironment):

    def __init__(self, game,  controller=None, **kwargs):
        GameEnvironment.__init__(self, game, visualize=True, **kwargs)
        self.controller = controller
        self.screen = SubjectiveSceen()
        self.screen._initScreen()
        self.reset()
        self.state = self.getState()
        self.eventHistory = list()

    def reset(self):
        GameEnvironment.reset(self)
        if hasattr(self, 'screen'):
            self.screen.reset()
            pygame.display.flip()

    def performAction(self, ACTION=None, action = None):
        if ACTION is None:
            self.setState(self.state)
            GameEnvironment.performAction(self, action)
            if action is not None:
                self._drawState()
                pygame.time.wait(self.actionDelay)
            self.eventHistory.append(action)
            self.state = self.getState()
        else:
            GameEnvironment.performAction(self, ACTION)




    def _nearTileIncrements(self):
        p0, p1, orient = self.getState()[:3]
        o0, o1 = orient
        l0, l1 = BASEDIRS[(BASEDIRS.index(orient) + 1) % len(BASEDIRS)]
        r0, r1 = BASEDIRS[(BASEDIRS.index(orient) - 1) % len(BASEDIRS)]
        
        res = [(True, 1, (p0 + 2 * l0, p1 + 2 * l1)),
               (True, 2, (p0 + o0 + 2 * l0, p1 + o1 + 2 * l1)),
               (True, 3, (p0 + 2 * o0 + l0, p1 + 2 * o1 + l1)),
               (True, 4, (p0 + 2 * o0, p1 + 2 * o1)),
               (True, 5, (p0 + 2 * o0 + r0, p1 + 2 * o1 + r1)),
               (True, 6, (p0 + o0 + 2 * r0, p1 + o1 + 2 * r1)),
               (True, 7, (p0 + 2 * r0, p1 + 2 * r1)),
               (False, 2, (p0 + o0 + l0, p1 + o1 + l1)),
               (False, 4, (p0 + o0 + r0, p1 + o1 + r1)),
               (False, 3, (p0 + o0, p1 + o1)),
               (False, 1, (p0 + l0, p1 + l1)),
               (False, 5, (p0 + r0, p1 + r1)),
               (False, 6, (p0, p1)),
               ]
        return res

    def _drawState(self):
        self.screen.reset()
        for iswall, fid, pos in self._nearTileIncrements():
            for oname, ps in self._obstypes.items():
                b = (oname in blocky)
                col = self._obscols[oname]
                if pos in ps:
                    if iswall:
                        self.screen._colorWall(fid, col)
                    elif not b:
                        self.screen._colorFloor(fid, col)
                    else:
                        self.screen._colorBlock(fid, col)
        pygame.display.flip()  

    