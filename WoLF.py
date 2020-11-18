import random

class WoLF:

    def __init__(self, player, alpha, gamma, delta_win, delta_lose, num_states, num_actions):
        self.player = player
        self.alpha = alpha
        self.delta_win = delta_win
        self.delta_lose = delta_lose
        self.gamma = gamma
        self.num_actions = num_actions
        self.Q = [[0] * num_actions for _ in range(num_states)]
        self.pi = [[1/num_actions] * num_actions for _ in range(num_states)]
        self.C = [0 for _ in range(num_states)]
        self.last_state = -1
        self.avpi = [[1/num_actions] * num_actions for _ in range(num_states)]

    def getMove(self,lastReward, lastMove):
        value = self.select_action()
        return value

    def select_action(self):
        state = self.last_state
        if state == -1:
            choice = random.choice(range(self.num_actions))
            return choice
        target = random.random()
        collect = self.pi[state][0]
        if target < collect:
            return 0
        for i in range(1, len(self.pi[state])):
            collect += self.pi[state][i]
            if target < collect:
                return i
        return self.num_actions-1

    def update(self, own, other, reward):
        state = own*2 + other
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
                self.pi[self.last_state][own] += delta
            else:
                self.pi[self.last_state][own] += (-delta / (self.num_actions-1))
            if self.pi[self.last_state][own] < 0:
                self.pi[self.last_state][own] = 0
            elif self.pi[self.last_state][own] > 1:
                self.pi[self.last_state][own] = 1
        self.last_state = state
        #self.printpi()

    def getPlayer(self):
        return self.player

    def printpi(self):
        print("Player: ", self.player, self.pi)

    def printQpi(self, state, action):
        print(self.Q[state][action])
        print(self.pi[state][action])




#Wolf = WoLF(1, 0.1, 0.9, 0.3, 0.1, 5, 2)
#Wolf.printQpi(4, 1)