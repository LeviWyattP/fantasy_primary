import datetime
import data_stores as d


class State:

    def __init__(self, state, date_of_primary, results):
        self.name = state
        self.primary_date = date_of_primary
        self.results = results


class Candidate:
    def __init__(self, name, stock_price_modifier):
        self.name = name
        self.delegates, self.popular_vote = -1
        self.shares = 10
        self.stock_price_modifier = stock_price_modifier
        self.stock_price = 0
        self.set_stock_price()

    def buy_candidate_stock(self, player_money):

        # if there are shares available and the player has enough money
        if self.shares > 0:
            # if shares are available - the share is bought. Reduce total shares by one.
            self.shares = self.shares - 1
        elif player_money < self.get_stock_price():
            # -1 means not enough money
            return -1
        elif self.shares <= 0:
            # -2 means that there are not shares available
            return -2
        else:
            # -3 no idea what happened
            return -3

    def sell_candidate_stock(self, player_money):

        # what is the price of the stock - this is what the player will get
        # Then add a share and set a new price
        player_money = self.get_stock_price()
        self.shares += 1
        self.set_stock_price()

        return player_money

    def set_stock_price(self):
        self.stock_price = 1 * self.stock_price_modifier ** (11 - self.get_shares())

    def get_stock_price(self):
        return self.stock_price

    def get_shares(self):
        return self.shares


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.delegates = 0
        self.total_votes = 0

        # stocks. Key = name; result = number of stocks
        self.stocks = {}

    def add_stock(self, candidate_select):
        candidate_select.buy_candidate_stock()

    def sell_stock(self, candidate_select):

        # Check for number of stocks - Does the player have stock in this candidate
        number_of_stocks = self.check_for_stock(candidate_select)

        # if we have stocks to sell - let's sell
        if number_of_stocks > 0:

            # sell stock, get the money back, add it to total players money
            money_gained = candidate_select.sell_candidate_stock()
            self.money += money_gained

    def check_for_stock(self, candidate_name):

        stocks = self.stocks.keys()
        if candidate_name in stocks:

            # Since we have (or have had)a stock - lets check for the number of stocks.
            # This can be zero
            number_of_stocks = self.stocks[candidate_name]

        else:
            # the player has no stock in this candidate
            number_of_stocks = 0

        return number_of_stocks

candidates_list = []

# To-Do: Need to refine logic and approach for 'results' component -LD
iowa = State("Iowa", datetime.date(2016, 2, 1))
for candidate in d.candidates:
    candidates_list.append(Candidate(candidate))

results_for_2016 = {}

# results_for_2016['IOWA']
