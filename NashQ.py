import random
import numpy as np
import nashpy as nash
from collections import defaultdict

class NashQ:

    def __init__(self, player, alpha, gamma,epsilon, num_states, num_actions):
        self.player = player
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_actions = num_actions
        self.base_alpha = alpha
        self.Q = np.zeros((2, num_states, self.num_actions, self.num_actions))
        self.last_state = -1
        self.history_alpha = np.zeros((num_states, self.num_actions, self.num_actions))
        self.history_act = np.zeros((num_states, 1))


    def getMove(self,lastReward, lastMove, tick):
        value = self.select_action(tick)
        return value

    """calculate actions a^i_t"""
    def select_action(self,tick):
        state = self.last_state
        if random.random() < self.epsilon:
            choice = np.random.choice(np.arange(self.num_actions), 1)[0]
        else:
            # print(self.Q)
            # print("unravel",np.unravel_index(np.argmax(self.Q[0, state], axis=None), self.Q[0, state].shape))
            # choice = np.unravel_index(np.argmax(self.Q[0, state], axis=None), self.Q[0, state].shape)[0]
            # print("chouche unravel,",choice)
            A = self.Q[0, state]
            B = self.Q[1, state]
            rps = nash.Game(A, B)
            eqs = list(rps.support_enumeration())
            eqs_0 = eqs[0][0].tolist()
            choice = np.random.choice(np.arange(len(eqs_0)), p=eqs_0)
        return choice

    #get nash Equilibrium
    def nash_action(self,state):
        A = self.Q[0, state]
        B = self.Q[1, state]
        rps = nash.Game(A, B)
        # print(rps)
        choices = [0, 0]
        eqs = list(rps.support_enumeration())
        nash_length = len(eqs)
        try:
            # nash_choice = np.random.choice(np.arange(nash_length), 1)[0]  #Random choice of Nash-equilibrium
            nash_choice = 0
            eqs_0 = eqs[nash_choice][0].tolist()
            # print("Eqssss", eqs_0)
            choices[0] = np.random.choice(np.arange(len(eqs_0)), p=eqs_0)
            eqs_1 = eqs[nash_choice][1].tolist()
            # print("Eqssss1", eqs_1)
            choices[1] = np.random.choice(np.arange(len(eqs_1)), p=eqs_1)
            # return [eqs_0, eqs_1]
            # if choices[0]==1 or choices[1]==1:
            return choices
        except IndexError:
            return [None, None]

    def update(self, own, other,nash_actions, state, rewards):
        self.history_alpha[state, own, other] += 1
        nash_actions_local = nash_actions[self.player]
        V = np.zeros(2)
        if None not in nash_actions_local:
            V[0] = self.Q[0, state, nash_actions_local[0], nash_actions_local[1]]
            V[1] = self.Q[1, state, nash_actions_local[1], nash_actions_local[0]]
            # print("V",V)
            # for i in range(len(nash_actions_local)):
            #     for j in range(len(nash_actions_local)):# it's probabilities now
            #         V[0] += self.Q[0, state, i, j]*nash_actions[0][i]*nash_actions[1][j]
            # for i in range(len(nash_actions_local)):
            #     for j in range(len(nash_actions_local)):# it's probabilities now
            #         V[1] += self.Q[1, state, j, i]*nash_actions[0][i]*nash_actions[1][j]
        else:
            V[0] = self.val(state, 0)
            V[1] = self.val(state, 1)

        alpha = self.base_alpha / (self.history_alpha[state, own, other])

        #  Qit+1(s;a1; : : : ;an) = (1−alpha) * Qit(s;a1, a2)+         alpha * [rit     +          gamma * (NashQit(s')]
        self.Q[0, state, own, other] = (1 - alpha) * self.Q[0, state, own, other] + alpha * (rewards[self.player] + self.gamma * V[0])
        self.Q[1, state, other, own] = (1 - alpha) * self.Q[1, state, other, own] + alpha * (rewards[1 - self.player] + self.gamma * V[1])

            # except ValueError:
            #     print(V)
            #     print(nash_actions_local)
            #     print(nash_actions)



#
    def getPlayer(self):
        return self.player

    def val(self, state, player_num):
        return np.max(self.Q[player_num, state])




#Wolf = WoLF(1, 0.1, 0.9, 0.3, 0.1, 5, 2)
#Wolf.printQpi(4, 1)