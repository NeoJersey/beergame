import random
import numpy as np
import nashpy as nash

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
        # pi, pi_o = self.compute_pi(state)
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

            # choice = np.random.choice(np.flatnonzero(pi == pi.max()))
        return choice

    #get nash Equilibrium
    def nash_action(self, state, pi, pi_o,q):
        # A = self.Q[0, state]
        # B = self.Q[1, state]
        # rps = nash.Game(A, B)
        # # print(rps)
        # choices = [0, 0]
        # eqs = list(rps.support_enumeration())
        # nash_length = len(eqs)
        # try:
        #     # nash_choice = np.random.choice(np.arange(nash_length), 1)[0]  #Random choice of Nash-equilibrium
        #     nash_choice = 0
        #     eqs_0 = eqs[nash_choice][0].tolist()
        #     # print("Eqssss", eqs_0)
        #     choices[0] = np.random.choice(np.arange(len(eqs_0)), p=eqs_0)
        #     eqs_1 = eqs[nash_choice][1].tolist()
        #     # print("Eqssss1", eqs_1)
        #     choices[1] = np.random.choice(np.arange(len(eqs_1)), p=eqs_1)
        #     # return [eqs_0, eqs_1]
        #     # if choices[0]==1 or choices[1]==1:
        #     return choices
        # except IndexError:
        #     return [None, None]
        nashq = 0
        for action1 in range(self.num_actions):
            for action2 in range(self.num_actions):
                nashq += pi[action1] * pi_o[action2] * \
                         q[state][(action1, action2)]
        # print(nashq)
        return nashq

    def update(self, own, other, nash_action, q, reward, state):
        self.history_alpha[state, own, other] += 1
        q_old = q[0, own, other]
        self.alpha = self.base_alpha / (self.history_alpha[state, own, other])
        # self.alpha = 1 / (self.history_alpha[state, own, other])
        if self.alpha < 0.001:
            self.alpha = 0.001
        updated_q = q_old + \
                    (self.alpha * (reward + (self.gamma * nash_action) - q_old))

        return updated_q

        # self.history_alpha[state, own, other] += 1
        # nash_actions_local = nash_actions[self.player]
        # V = np.zeros(2)
        # if None not in nash_actions_local:
        #     V[0] = self.Q[0, state, nash_actions_local[0], nash_actions_local[1]]
        #     V[1] = self.Q[1, state, nash_actions_local[1], nash_actions_local[0]]
        #     # print("V",V)
        #     # for i in range(len(nash_actions_local)):
        #     #     for j in range(len(nash_actions_local)):# it's probabilities now
        #     #         V[0] += self.Q[0, state, i, j]*nash_actions[0][i]*nash_actions[1][j]
        #     # for i in range(len(nash_actions_local)):
        #     #     for j in range(len(nash_actions_local)):# it's probabilities now
        #     #         V[1] += self.Q[1, state, j, i]*nash_actions[0][i]*nash_actions[1][j]
        # else:
        #     V[0] = self.val(state, 0)
        #     V[1] = self.val(state, 1)
        #
        # alpha = self.base_alpha / (self.history_alpha[state, own, other])
        #
        # #  Qit+1(s;a1; : : : ;an) = (1−alpha) * Qit(s;a1, a2)+         alpha * [rit     +          gamma * (NashQit(s')]
        # self.Q[0, state, own, other] = (1 - alpha) * self.Q[0, state, own, other] + alpha * (rewards[self.player] + self.gamma * V[0])
        # self.Q[1, state, other, own] = (1 - alpha) * self.Q[1, state, other, own] + alpha * (rewards[1 - self.player] + self.gamma * V[1])


    def compute_pi(self, state):
        """
            compute pi (nash)
        """
        # q_1, q_2 = [], []
        # for action1 in range(self.num_actions):
        #     row_q_1, row_q_2 = [], []
        #     for action2 in range(self.num_actions):
        #         joint_action = (action1, action2)
        #         row_q_1.append(self.Q[0,state,action1,action2])
        #         row_q_2.append(self.Q[1,state,action1,action2])
        #
        #     q_1.append(row_q_1)
        #     q_2.append(row_q_2)

        q_1 = self.Q[0, state]
        q_2 = self.Q[1, state]
        game = nash.Game(q_1, q_2)
        equilibria = game.support_enumeration()
        # equilibria = game.lemke_howson_enumeration()
        # equilibria = game.vertex_enumeration()
        pi_list = list(equilibria)

        pi = None
        for _pi in pi_list:
            if _pi[0].shape == (self.num_actions, ) and _pi[1].shape == (
                    self.num_actions, ):
                if any(
                    np.isnan(
                        _pi[0])) is False and any(
                    np.isnan(
                        _pi[1])) is False:
                    pi = _pi
                    break

        if pi is None:
            pi1 = np.repeat(
                1.0 / self.num_actions, self.num_actions)
            pi2 = np.repeat(
                1.0 / self.num_actions, self.num_actions)

            pi = (pi1, pi2)

        return pi[0], pi[1]

#
    def getPlayer(self):
        return self.player

    def val(self, state, player_num):
        return np.max(self.Q[player_num, state])




#Wolf = WoLF(1, 0.1, 0.9, 0.3, 0.1, 5, 2)
#Wolf.printQpi(4, 1)