map = """
wwwwwwwwwwww
wG        <w
w www<wwww w
w----    w w
www- ww<=w w
w    w^== ^w
w  ===== www
wA =======^w
wwwwwwwwwwww
"""

rules = """
BasicGame 
    LevelMapping
        - > wind
        = > ice
        G > goal
        < > tvleft
        ^ > tvup
        
    SpriteSet         
        structure > Immovable
            goal  > color=GREEN
            tv    > Conveyor color=RED
                tvup    > orientation=UP
                tvleft  > orientation=LEFT
            ice   > color=WHITE
            wind  > Conveyor orientation=RIGHT strength=1                                         
        avatar   > RotatingAvatar

    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
        
    InteractionSet
        goal avatar  > killSprite
        avatar wind  > windGust
        avatar tv    > attractGaze prob=1
        avatar ice   > slipForward prob=0.3
        avatar wall  > stepBack        
"""


def main():
    from vgdl.core import VGDLParser
    from MCTSPlayer.Agent import Agent
    from RandomRuleGenerator.RandomRuleGenerator import RandomRuleGenerator
    from aiGame import aiGame
    from Timer import ElapsedCPUTimer

    # parse, run and play.
    parser = VGDLParser()
    game = parser.parseGame(rules)
    game.buildLevel(map)


    # Creating timer state and controller
    timer = ElapsedCPUTimer()
    timer.setMaxTime(10)

    for i in range(0, 10):
        gen = RandomRuleGenerator(map, game, timer)
        interactions, terminations = gen.generateRuleSet(timer)
        interactionSTR = 'InteractionSet\n'
        terminationSTR = 'TerminationSet\n'

        for interaction in interactions:
            interactionSTR += '        ' + interaction + '\n'
        for termination in terminations:
            terminationSTR += '        ' + termination + '\n'

        newRules = """
BasicGame
    LevelMapping
        - > wind
        = > ice
        G > goal
        < > tvleft
        ^ > tvup
        
    SpriteSet         
        structure > Immovable
            goal  > color=GREEN
            tv    > Conveyor color=RED
                tvup    > orientation=UP
                tvleft  > orientation=LEFT
            ice   > color=WHITE
            wind  > Conveyor orientation=RIGHT strength=1                                         
        avatar   > RotatingAvatar
        
    %s
        avatar wall  > stepBack
        
    %s
""" % (interactionSTR, terminationSTR)
        print(map)

        print(newRules)
        game = parser.parseGame(newRules)
        game.buildLevel(map)

        game.startGame(False, False)


    return 0


if __name__ == '__main__':
    main()