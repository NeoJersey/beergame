import random

class BeerGame:

    def __init__(self):
        self.inv_R = 12
        self.inv_F = 12

        self.backlog_R = 0
        self.backlog_F = 0

        self.cost_inv = 0.5
        self.cost_backlog = 1

        self.demand_cus = [4,4,4]
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

        self.choices = [0,4,10,20,30]

        for i in range(len(self.demand_cus)):
            self.WeekLoop(i)
        self.print()

    def WeekLoop(self, i):
        #transfer
        self.inv_R += self.delay1_F
        self.inv_F += self.prod_delay1

        self.delay1_F = self.delay2_F
        self.prod_delay1 = self.prod_delay2

        #Fulfill orders
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
            
        
        #Transfer orders
        self.orders_incoming_F = self.orders_placed_R

        #Factory Orders
        self.prod_delay2 = self.prod_request
        
        #Players Choice
        self.orders_placed_R = self.ChooseRetail()
        self.prod_request = self.ChooseFactory()


        #Record Cost
        self.cost_R.append(self.inv_R*self.cost_inv + self.backlog_R*self.cost_backlog)
        self.cost_F.append(self.inv_F * self.cost_inv + self.backlog_F * self.cost_backlog)
        print("R: ", self.orders_placed_R, self.inv_R, self.backlog_R)
        print("F: ", self.prod_request, self.inv_F, self.backlog_F)

    def print(self):
        print("Cost R: ", self.cost_R, sum(self.cost_R))
        print("Cost F: ", self.cost_F, sum(self.cost_F))

    def ChooseRetail(self):
        if self.backlog_R == 0:
            #return 4
            return random.choice([self.choices[0], self.choices[1], self.choices[2]])
        else:
            #return 20
            return random.choice([self.choices[3], self.choices[4]])
        #return random.choice(self.choices)

    def ChooseFactory(self):
        if self.backlog_F == 0:
            #return 4
            return random.choice([self.choices[0], self.choices[1], self.choices[2]])
        else:
            #return 20
            return random.choice([self.choices[3], self.choices[4]])

def main():
    newGame = BeerGame()

if __name__ == "__main__":
    main()
