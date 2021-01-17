import Human, TestPlayer, WoLF, distribution
from NashQ import NashQ
import numpy as np
import random
import nashpy as nash
METHOD = "WoLF"
# METHOD = "NashQ"

# REPEATED_ACTION_TYPE = 1 #No repeated action pairs are applied
# REPEATED_ACTION_TYPE = 2 #Repeated action pairs applied n times, where n is a value coming from poisson distribution
REPEATED_ACTION_TYPE = 3  # specific move repeated with lambda probability
if REPEATED_ACTION_TYPE == 3:
    LAMBDA_VALUE = 0.3
    FORCED_ACTION = [0,0]

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
        action_forced = 0
        players = [self.playerOne, self.playerTwo]
        actions = []
        nash_actions = []
        rewards = self.getMovesReward(onePick, twoPick)
        while(self.tick < 10000):

            if not REPEATED_ACTION_TYPE == 2:  # activate or deactivate repeated action pairs
                self.nextMove = self.tick

            if METHOD == 'WoLF':
                if self.tick == self.nextMove:
                    updateCount += 1
                    if REPEATED_ACTION_TYPE == 3 and random.random() < LAMBDA_VALUE:
                        action_forced += 1
                        onePick, twoPick = FORCED_ACTION
                        print("action forced", FORCED_ACTION)
                    else:
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
                    if REPEATED_ACTION_TYPE == 3 and random.random() < LAMBDA_VALUE:
                        action_forced += 1
                        actions = FORCED_ACTION
                        print("action repeated", FORCED_ACTION)
                    else:
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
        print(f"Number of forced actions: {action_forced}")
        print("player 1 played:", int(self.countMoves[0][0]), int(self.countMoves[0][1]))
        print("player 2 played:", int(self.countMoves[1][0]), int(self.countMoves[1][1]))
        # self.playerOne.printpi()
        # self.playerTwo.printpi()
        #onePick*2+twoPick

def main():
    # newGame = Game([5,5], [6,0],
    #                [0,6], [1,1]) #prisoner dilemma
    newGame = Game([1,-1], [-1,1], [-1,1], [1,-1]) #matching pennies

    # print(newGame)
    # print(newGame.getMoveValues(0, 1))
    # print("reward",newGame.getMoveReward(0, 1, 1))
    newGame.startLoop()

if __name__ == "__main__":
    main()