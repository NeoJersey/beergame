class TestPlayer:

    def __init__(self, player):
        self.average = 0
        self.count = 0
        self.player = player
        pass

    def getMove(self, lastReward, lastMove):
        if lastReward > self.average:
            move = lastMove[self.player]
        else:
            move = abs(lastMove[self.player]-1)
        print(self.player, lastReward, lastMove)
        self.newAverage(lastReward)
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