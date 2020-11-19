import Human, TestPlayer, WoLF, distribution

class Game:

    def __init__(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.game = [[self.topLeft, self.topRight], [self.bottomLeft, self.bottomRight]]
        self.distr = distribution.distribution()
        self.playerOne = WoLF.WoLF(0, 0.2, 0.9, 0.05, 0.15, 4, 2)
        self.playerTwo = WoLF.WoLF(1, 0.2, 0.9, 0.05, 0.15, 4, 2)
        self.tick = 0


    def getMoveReward(self, onePick, twoPick, player):
        return self.game[onePick][twoPick][player]

    def getMoveValues(self, onePick, twoPick):
        return self.game[onePick][twoPick]

    def startLoop(self):
        onePick = self.playerOne.getMove(0, [0,0])
        twoPick = self.playerTwo.getMove(0, [0,0])
        self.tick += 1
        self.nextMove = self.tick + self.distr.getNext()
        self.loop(onePick, twoPick)

    def loop(self, onePick, twoPick):
        while(self. tick < 100000):
            if self.tick == self.nextMove:
                onePick = self.playerOne.getMove(self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), [onePick, twoPick])
                twoPick = self.playerTwo.getMove(self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()), [onePick, twoPick])
                self.nextMove = self.tick + self.distr.getNext()
                print("Player 0: ", "Pick: ", onePick, "Reward:",self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), "Tick: ", self.tick)
                print("Player 1: ", "Pick: ", twoPick, "Reward:",self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))
            self.playerOne.update(onePick, twoPick, self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()))
            self.playerTwo.update(twoPick, twoPick, self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()))
            self.tick += 1
        print("Player 0: ","Pick: ", onePick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), "Tick: " ,self.tick)
        print("Player 1: ","Pick: ", twoPick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))
        self.playerOne.printpi()
        self.playerTwo.printpi()


def main():
    newGame = Game([-3,-3], [0,-5], [-5,0], [-1,-1])
    print(newGame.getMoveValues(0,1))
    print(newGame.getMoveReward(0,1,1))
    newGame.startLoop()


if __name__ == "__main__":
    main()