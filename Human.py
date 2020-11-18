class Human:

    def __init__(self, player):
        self.average = 0
        self.count = 0
        self.player = player

    def getMove(self, lastReward, lastMove):
        self.newAverage(lastReward)
        move = int(input("Pick Move 0 or 1: "))
        while not (move == 1 or move == 0):
            move = int(input("Pick Move 0 or 1: "))
        return move

    def getPlayer(self):
        return self.player

    def newAverage(self, reward):
        if self.count == 0:
            self.count +=1
        elif self.count == 1:
            self.average = reward
            self.count +=1
        else:
            self.count+=1
            self.average = self.average + ((reward-self.average)/self.count)
        print("Average Reward: ",self.average, self.player)