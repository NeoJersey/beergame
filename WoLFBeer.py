import random

class WoLFBeer:

    def __init__(self, player, alpha, gamma, delta_win, delta_lose, choices):
        self.player = player
        self.alpha = alpha
        self.gamma = gamma
        self.delta_win = delta_win
        self.delta_lose = delta_lose
        self.choices = choices
        self.num_actions = len(choices)
        self.Q = [random.random()] * self.num_actions
        self.pi = [1/self.num_actions] * self.num_actions
        self.C = 0
        self.avPi = [0.0] * self.num_actions

    def getMove(self, tick):
        chance = random.random()
        if tick == 0 or chance < 1/tick:
            choice = random.choice(self.choices)
            return choice
        target = random.random()
        collect = 0
        sumProbs = sum(self.pi)
        for i in range(len(self.pi)):
            collect += self.pi[i]/sumProbs
            if target < collect:
                return self.choices[i]

    def update(self, choice, reward):
        myIndex = self.choices.index(choice)
        self.Q[myIndex] = (1-self.alpha) * self.Q[myIndex] + self.alpha * (reward + self.gamma * max(self.Q))
        self.C += 1

        for i in range(self.num_actions):
            self.avPi[i] = self.avPi[i] + (1/self.C) * (self.pi[i] - self.avPi[i])

        sumPi = 0
        sumAvPi = 0

        for i in range(self.num_actions):
            sumPi += self.pi[i] * self.Q[i]
            sumAvPi += self.avPi[i] * self.Q[i]

        if sumPi > sumAvPi:
            delta = self.delta_win
        else:
            delta = self.delta_lose

        if self.Q.index(max(self.Q)) == myIndex:
            for i in range(self.num_actions):
                if i == myIndex:
                    self.pi[i] += delta
                else:
                    self.pi[i] += -(delta/(self.num_actions-1))
        else:
            if i == myIndex:
                self.pi[i] += (-delta/(self.num_actions-1))
            else:
                self.pi[i] += -((-delta/(self.num_actions-1)) / (self.num_actions - 1))

        for i in range(self.num_actions):
            if self.pi[i] > 1:
                self.pi[i] = 1
            elif self.pi[i] < 0:
                self.pi[i] = 0

    def debug(self):
        print("Player: ", self.player, "Pi values: ", self.pi, "Q:", self.Q)