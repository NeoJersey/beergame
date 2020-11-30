import random

class WoLF:

    def __init__(self, player, alpha, gamma, delta_win, delta_lose, num_states, num_actions):
        self.player = player
        self.alpha = alpha
        self.delta_win = delta_win
        self.delta_lose = delta_lose
        self.gamma = gamma
        self.num_actions = num_actions
        self.Q = [[0.0] * num_actions for _ in range(num_states)]
        self.pi = [[1/num_actions] * num_actions for _ in range(num_states)]
        self.C = [0 for _ in range(num_states)]
        self.last_state = -1
        self.avpi = [[0.0] * num_actions for _ in range(num_states)]

    def getMove(self,lastReward, lastMove, tick):
        value = self.select_action(tick)
        return value


    def select_action(self, tick):
        state = self.last_state
        self.printpi()
        chance = random.random()
        if state == -1 or chance < 1/tick:
            choice = random.choice(range(self.num_actions))
            return choice
        target = random.random()
        collect = 0
        sumProbs = sum(self.pi[state])
        if sumProbs == 0:
            choice = random.choice(range(self.num_actions))
            return choice
        for i in range(len(self.pi[state])):
            collect += self.pi[state][i]/sumProbs
            if target < collect:
                return i
        return self.num_actions-1

    #TODO Update when?
    def update(self, own, state, reward):
        if self.last_state != -1:
            self.Q[self.last_state][own] = (1-self.alpha)*self.Q[self.last_state][own] + self.alpha * (reward + self.gamma * max(self.Q[state]))
            self.C[self.last_state] += 1
            for i in range(len(self.avpi[self.last_state])):
                self.avpi[self.last_state][i] = self.avpi[self.last_state][i] + (1/self.C[self.last_state])* (self.pi[self.last_state][i] - self.avpi[self.last_state][i])
            sumPi = 0
            sumAvpi = 0
            for i in range(self.num_actions):
                sumPi += self.pi[self.last_state][i] * self.Q[self.last_state][i]
                sumAvpi += self.avpi[self.last_state][i] * self.Q[self.last_state][i]
            if sumPi > sumAvpi:
                delta = self.delta_win
            else:
                delta = self.delta_lose
            if self.Q[state].index(max(self.Q[state])) == own:
                #print("Check")
                self.pi[self.last_state][own] += delta
            else:
                self.pi[self.last_state][own] += (-delta / (self.num_actions-1))
            if self.pi[self.last_state][own] < 0:
                self.pi[self.last_state][own] = 0
            elif self.pi[self.last_state][own] > 1:
                self.pi[self.last_state][own] = 1
        self.last_state = state
        self.printpi()

    def updateQ(self, own, state, reward):
        self.Q[self.last_state][own] = (1 - self.alpha) * self.Q[self.last_state][own] + self.alpha * (reward + self.gamma * max(self.Q[state]))

    def getPlayer(self):
        return self.player

    def printpi(self):
        print("Player: ", self.player, "Pi values: ", self.pi, "Q:", self.Q)

    def printQpi(self, state, action):
        print(self.Q[state][action])
        print(self.pi[state][action])




#Wolf = WoLF(1, 0.1, 0.9, 0.3, 0.1, 5, 2)
#Wolf.printQpi(4, 1)