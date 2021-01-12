import random, WoLFBeer, SarsaBeer


class BeerGame:

    def __init__(self):
        self.inv_R = 12
        self.inv_F = 12

        self.backlog_R = 0
        self.backlog_F = 0

        self.cost_inv = 0.5
        self.cost_backlog = 1

        self.demand_cus = [4, 4, 4]
        for _ in range(49):
            self.demand_cus.append(8)

        self.orders_incoming_F = 4
        self.orders_placed_R = 4
        self.prod_request = 4
        self.delay2_F = 4
        self.delay1_F = 4
        self.prod_delay2 = 4
        self.prod_delay1 = 4

        self.cost_R = []
        self.cost_F = []

        self.choices = [0, 4, 10, 20, 30]

        self.Retailer = SarsaBeer.SarsaBeer("Retailer", 0.5, 0.9, 0.1, self.choices, 6, 5, 4)
        self.Factory = SarsaBeer.SarsaBeer("Factory", 0.5, 0.9, 0.1, self.choices, 6, 5, 4)
        weeks = 10000
        for j in range(weeks):
            for i in range(len(self.demand_cus)):
                self.WeekLoop(i, i*j)
            if j % (weeks/10) == 0 or j == weeks - 1:
                self.print(j)
            self.Initial()

    def Initial(self):
        self.inv_R = 12
        self.inv_F = 12

        self.backlog_R = 0
        self.backlog_F = 0
        self.orders_incoming_F = 4
        self.orders_placed_R = 4
        self.prod_request = 4
        self.delay2_F = 4
        self.delay1_F = 4
        self.prod_delay2 = 4
        self.prod_delay1 = 4

        self.cost_R = []
        self.cost_F = []

    def WeekLoop(self, i, tick):
        # transfer
        self.inv_R += self.delay1_F
        self.inv_F += self.prod_delay1

        self.delay1_F = self.delay2_F
        self.prod_delay1 = self.prod_delay2

        # Fulfill orders
        if self.inv_R >= self.demand_cus[i] + self.backlog_R:
            self.inv_R -= self.demand_cus[i] + self.backlog_R
            self.backlog_R = 0
        else:
            self.backlog_R = self.demand_cus[i] + self.backlog_R - self.inv_R
            self.inv_R = 0

        if self.inv_F >= self.orders_incoming_F + self.backlog_F:
            self.inv_F -= self.orders_incoming_F + self.backlog_F
            self.delay2_F = self.orders_incoming_F + self.backlog_F
            self.backlog_F = 0
        else:
            self.backlog_F = self.orders_incoming_F + self.backlog_F - self.inv_F
            self.delay2_F = self.inv_F
            self.inv_F = 0

        # Transfer orders
        self.orders_incoming_F = self.orders_placed_R

        # Factory Orders
        self.prod_delay2 = self.prod_request

        # Player Updates
        curr_cost_R = self.inv_R * self.cost_inv + self.backlog_R * self.cost_backlog
        curr_cost_F = self.inv_F * self.cost_inv + self.backlog_F * self.cost_backlog


        # Players State
        if self.inv_R == 0:
            r_state = 0
        else:
            if self.inv_R > 100:
                r_state = 2
            elif self.inv_R > 50:
                r_state = 3
            elif self.inv_R > 25:
                r_state = 4
            elif self.inv_R > 10:
                r_state = 5
            else:
                r_state = 1
        if self.inv_F == 0:
            f_state = 0
        else:
            if self.inv_F > 100:
                f_state = 2
            elif self.inv_F > 50:
                f_state = 3
            elif self.inv_F > 25:
                f_state = 4
            elif self.inv_F > 10:
                f_state = 5
            else:
                f_state = 1


        # Players Choice and Update
        self.orders_placed_R = self.Retailer.update(-curr_cost_R, r_state, tick)
        self.prod_request = self.Factory.update(-curr_cost_F, f_state, tick)

        # Record Cost
        self.cost_R.append(curr_cost_R)
        self.cost_F.append(curr_cost_F)

        if (False):
            print("R: ", self.orders_placed_R, self.inv_R, self.backlog_R)
            #print("F: ", self.prod_request, self.inv_F, self.backlog_F)

    def print(self,j):
        print("Iteration: ", j)
        print("Cost R: ", sum(self.cost_R),self.cost_R)
        print("Cost F: ", sum(self.cost_F),self.cost_F)
        self.Retailer.debug()
        self.Factory.debug()

    def ChooseRetail(self):
        if self.backlog_R == 0:
            # return 4
            return random.choice([self.choices[0], self.choices[1], self.choices[2]])
        else:
            # return 20
            return random.choice([self.choices[3], self.choices[4]])
        # return random.choice(self.choices)

    def ChooseFactory(self):
        if self.backlog_F == 0:
            # return 4
            return random.choice([self.choices[0], self.choices[1], self.choices[2]])
        else:
            # return 20
            return random.choice([self.choices[3], self.choices[4]])


def main():
    newGame = BeerGame()


if __name__ == "__main__":
    main()
