import random


class RandomRuleGenerator:

    def __init__(self, level, game, Timer):
        self.level = level
        self.usefulSprites = list()
        lines = [l for l in self.level.split("\n") if len(l) > 0]
        lengths = list(map(len, lines))

        'Adding useful sprites'
        for row, l in enumerate(lines):
            for col, c in enumerate(l):
                if c is not ' ':
                    if c in game.char_mapping:
                        spriteName = game.char_mapping[c][0]
                    elif c in game.default_mapping:
                        spriteName = game.default_mapping[c][0]

                    if spriteName not in self.usefulSprites and spriteName:
                        self.usefulSprites.append(spriteName)

        self.usefulSprites.append("EOS")
        self.avatar = game.getAvatars()
        self.interactions = ["killSprite", "killIfFromAbove", "stepBack", "cloneSprite", "transformTo", "undoAll",
                             "flipDirection", "reverseDirection", "attractGaze",
                             "turnAround", "wrapAround", "bounceForward", "collectResource",
                             "undoAll", "reverseDirection"]

    def generateRuleSet(self, timer):
        interactions = list()
        terminations = list()

        numberOfInteractions = int(len(self.usefulSprites) * (0.5 + 0.5 * random.random()))

        'Generation random interactions'
        for x in range(0, numberOfInteractions):
            'Determine which two objects to interact'
            interaction1 = random.choice(self.usefulSprites)
            interaction2 = random.choice(self.usefulSprites)

            scoreChange = ""

            'Add a score change if needed'
            if bool(random.getrandbits(1)):
                scoreChange += "scoreChange=" + str(random.randint(0, 5) - 2)

            'Choose a random interaction that is available'
            inter = random.choice(self.interactions)
            interactions.append("avatar" + " " + interaction2 + " > " + inter + " " + scoreChange)

        'Adding termination criteria'
        if bool(random.getrandbits(1)):
            terminations.append("Timeout limit=" + str(20) + " win=True")
        else:
            chosen = random.choice(self.usefulSprites)
            terminations.append("SpriteCounter stype=" + chosen + " limit=0 win=True")

        'When the avatar dies, the player losese'
        terminations.append("SpriteCounter stype=" + self.avatar[0].name + " limit=0 win=False")

        return interactions, terminations