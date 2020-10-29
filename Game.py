import Human, TestPlayer

class Game:

    def __init__(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.game = [[self.topLeft, self.topRight], [self.bottomLeft, self.bottomRight]]
        self.playerOne = TestPlayer.TestPlayer(0)
        self.playerTwo = TestPlayer.TestPlayer(1)

    def getMoveReward(self, onePick, twoPick, player):
        return self.game[onePick][twoPick][player]

    def getMoveValues(self, onePick, twoPick):
        return self.game[onePick][twoPick]

    def startLoop(self):
        onePick = self.playerOne.getMove(0, [0,0])
        twoPick = self.playerTwo.getMove(0, [0,0])
        self.loop(onePick, twoPick)

    def loop(self, onePick, twoPick):
        while(True):
            onePick = self.playerOne.getMove(self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), [onePick, twoPick])
            twoPick = self.playerTwo.getMove(self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()), [onePick, twoPick])


newGame = Game([-3,-3], [0,-5], [-5,0], [-1,-1])
print(newGame.getMoveValues(0,1))
print(newGame.getMoveReward(0,1,1))
newGame.startLoop()