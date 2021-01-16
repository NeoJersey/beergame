import Human, TestPlayer, WoLF, distribution
from NashQ import NashQ
import numpy as np
import nashpy as nash
# METHOD = "WoLF"
METHOD = "NashQ"
REPEATED_ACTION = True

def updateNash(player, actions, nash_actions, rewards, tick):
    player.update(actions[player.player], actions[1 - player.player], nash_actions, 0, rewards)
    player.epsilon = 1 / tick
    return player

class Game:

    def __init__(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.game = [[self.topLeft, self.topRight], [self.bottomLeft, self.bottomRight]]
        print("game", self.game)
        self.distr = distribution.distribution()
        if METHOD == 'WoLF':
            self.playerOne = WoLF.WoLF(0, 0.5, 0.9, 0.05, 0.1, 1, 2)
            self.playerTwo = WoLF.WoLF(1, 0.5, 0.9, 0.05, 0.1, 1, 2)
        else:
            self.playerOne = NashQ(player=0, alpha=0.5, gamma=0.9, epsilon=0.5, num_states=1, num_actions=2)
            self.playerTwo = NashQ(player=1, alpha=0.5, gamma=0.9, epsilon=0.5, num_states=1, num_actions=2)
        self.tick = 0
        self.countMoves = np.zeros((2, 2)) # (n_player, num_actions)

    def getMoveReward(self, onePick, twoPick, player):
        return self.game[onePick][twoPick][player]

    def getMovesReward(self, onePick, twoPick):
        return self.game[onePick][twoPick]

    def getMoveValues(self, onePick, twoPick):
        return self.game[onePick][twoPick]

    def startLoop(self):
        onePick = self.playerOne.getMove(0, [0,0], 0)
        twoPick = self.playerTwo.getMove(0, [0,0], 0)
        self.tick += 1
        # self.playerOne.printpi()
        self.nextMove = self.tick + self.distr.getNext()
        self.loop(onePick, twoPick)

    def loop(self, onePick, twoPick):
        updateCount = 0
        players = [self.playerOne, self.playerTwo]
        actions = []
        nash_actions = []
        rewards = self.getMovesReward(onePick, twoPick)
        while(self.tick < 10000):

            if not REPEATED_ACTION:  # activate or deactivate repeated action pairs
                self.nextMove = self.tick

            if METHOD == 'WoLF':
                if self.tick == self.nextMove:
                    updateCount += 1
                    onePick = self.playerOne.getMove(self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), [onePick, twoPick], self.tick)
                    twoPick = self.playerTwo.getMove(self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()), [onePick, twoPick], self.tick)
                    self.nextMove = self.tick + self.distr.getNext()
                    print("Player 0: ", "Pick: ", onePick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), "Tick: ", self.tick)
                    print("Player 1: ", "Pick: ", twoPick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))
                self.playerOne.update(onePick, 0, self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()))
                self.playerTwo.update(twoPick, 0, self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))

            elif METHOD == 'NashQ':
                # calculate new action
                if self.tick == self.nextMove or self.tick == 1:
                    updateCount += 1
                    actions = []
                    #choose action
                    for player in players:
                        actions.append(player.select_action(self.tick))
                    self.nextMove = self.tick + self.distr.getNext()
                    onePick, twoPick = actions
                    print("Player 0: ", "Pick: ", onePick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), "Tick: ", self.tick)
                    print("Player 1: ", "Pick: ", twoPick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))
                    rewards = self.getMovesReward(onePick,twoPick)
                    nash_actions = []
                    # search nash strategy
                    for i, player in enumerate(players):
                        nash_actions.append(player.nash_action(0))
                players_update = []
                #observe and update
                for player in players:
                    players_update.append(updateNash(player, actions, nash_actions, rewards, self.tick))
                players = players_update

            self.countMoves[0, onePick] += 1
            self.countMoves[1, twoPick] += 1
            self.tick += 1
        print("Player 0: ","Pick: ", onePick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerOne.getPlayer()), "Tick: " ,self.tick)
        print("Player 1: ","Pick: ", twoPick, "Reward:", self.getMoveReward(onePick, twoPick, self.playerTwo.getPlayer()))
        print(f"Number of Selections: {updateCount}")
        print("player 1 played:", int(self.countMoves[0][0]), int(self.countMoves[0][1]))
        print("player 2 played:", int(self.countMoves[1][0]), int(self.countMoves[1][1]))
        # self.playerOne.printpi()
        # self.playerTwo.printpi()
        #onePick*2+twoPick

def main():
    # newGame = Game([2,2], [5,0], [0,5], [4,4]) #prisoner dilemma
    newGame = Game([1,-1], [-1,1], [-1,1], [1,-1]) #matching pennies

    # print(newGame)
    # print(newGame.getMoveValues(0, 1))
    # print("reward",newGame.getMoveReward(0, 1, 1))
    newGame.startLoop()

if __name__ == "__main__":
    main()