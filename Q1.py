from enum import Enum
import numpy as np
import scr.FigureSupport as FigureSupport

class CoinFlip(Enum):
    """ outcome of each coin flip"""
    HEADS = 1
    TAILS = 0

class Game:
    def __init__(self, id, heads_prob):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)

        self.heads_prob = heads_prob
        self._flipList = []

    def simulate(self, numberFlips):
        """ simulate a game of numberFlips coin flips """
        for i in range(numberFlips):
            toss = self._rnd.binomial(1, self.heads_prob)
            if toss == 1:
                toss = CoinFlip.HEADS # convert binary output to H
            else:
                toss = CoinFlip.TAILS
            self._flipList.append(toss) # convert binary output to T

    def get_payout(self):
        """ determine how many times desired series of coin flip arises
        and calculate payout"""
        payout = -250
        n = 0 # number of times that [Tails, Tails, Heads] occurs
        for i in range(len(self._flipList)-2):
            if self._flipList[i] == CoinFlip.TAILS and self._flipList[i+1] == CoinFlip.TAILS and self._flipList[i+2] == CoinFlip.HEADS:
                n +=1
        payout += 100*n
        return payout

class Simulation:
    def __init__(self, id, number_games, heads_prob):
        """

        :param id: cohort ID
        :param number_games: number of games, each of which consist of number of coin flips according to numberFlips
        :param heads_prob: probability of heads on coin toss
        """

        self._games = []
        self._payouts = []

        # simulate multiple games and populate lists
        for i in range(number_games):
            game = Game(id*number_games+i, heads_prob)
            self._games.append(game)

    def simulate(self, numberFlips):
        for game in self._games:
            game.simulate(numberFlips) # run each of the games included in the games list

            payout = game.get_payout() # calculate payout for each game in the list
            self._payouts.append(payout) # add payout for each game to payouts list

    def get_payouts(self):
        return self._payouts

    def get_max(self):
        return max(self._payouts)

    def get_min(self):
        return min(self._payouts)

    def get_expected_value(self):
        return sum(self._payouts)/len(self._payouts)

    def get_probability_of_loss(self):
    # calculate the probability of losing money in this game
        numberlosses = 0
        for i in range(len(self._payouts)):
            if self._payouts[i] < 0:
                numberlosses += 1

        return numberlosses/len(self._games)

NUMBER_GAMES = 1000 # number of games within each simulation

NUMBER_FLIPS = 20 # number of coin flips within each game
HEADS_PROB = 0.5 # probability of heads

# Create simulation called myMoney
myMoney = Simulation(1, NUMBER_GAMES, HEADS_PROB)

# Run each game within myMoney
myMoney.simulate(NUMBER_FLIPS)

# Print expected value
print(myMoney.get_expected_value())

# Print minimum and maximum
print('The maximum reward is', myMoney.get_max())
print('The minimum reward is', myMoney.get_min())

# Generate histogram
FigureSupport.graph_histogram(
    observations= myMoney.get_payouts(),
    title= 'Histogram of Payouts',
    x_label= 'Payouts ($)',
    y_label= 'Number of games'
)
print('The minimum and maximum reward are -250 and +250, respectively')

# Generate probability of losing money
print('The probability of a loss in this game is', myMoney.get_probability_of_loss())

