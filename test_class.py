import datetime
import data_stores as data

max_stocks_for_candidate = 10
class State:

    def __init__(self, state, date_of_primary, results, unique_primaries):
        self.name = state
        self.primary_date = date_of_primary
        self.results = results

        # Do they have standard primary rules? Or specific
        self.primary_rules = self.check_primary_rules(unique_primaries)

        self.results_dict = {}

        # init class without results flag
        self.has_results = False

    def check_primary_rules(self, unique_primaries):

        # if the state is in the list of states with unique primary rules,
        # then set a flag that they have unique rules, other wise, its straight proportional
        if self.name in unique_primaries:
            self.primary_rules = False
        else:
            self.primary_rules = True

    def update_results(self, updated_results):
        self.results_dict = updated_results

        # set results flag - this lets us know if there are results
        number_of_candidates = len(self.results_dict.keys())
        if self.has_results == False:
            if number_of_candidates> 0:

                #looks like we at least have candidates - do any of them have votes? let's check
                for candidate in self.results_dict:
                    votes = self.results_dict[candidate][1]
                    if int(votes) > 0:
                        self.has_results = True

    def calculate_character_votes(self, player):

        votes = 0
        for each_candidate in player.stocks:

            # The percent vote share for the individual is the number of stocks they have divided by the total
            # possible stocks for candidates.
            percent_share = player.stocks[each_candidate] / max_stocks_for_candidate

            votes_for_candidate = self.results_dict[each_candidate][1]

            votes = votes + votes_for_candidate



    def calculate_delegates_for_players(self, all_players, state):

        total_votes = 0
        delegate_dict = {}

        # generic proportional distribution
        if not state.primary_rules:

            # get total votes
            for each_player in all_players:
               total_votes += each_player.state_votes[state.name]

            # now that we have the total votes - lets go back and calculate the delegate for each player
            for each_player in all_players:

                vote_share = each_player.state_votes[state.name]
                # TODO does rounding work out and make the delegate counts consistent??
                delegate_dict[each_player.name] = [round(vote_share/total_votes), vote_share]
        else:
            # TODO write code for individual primary rules?
            print('I havent writte this could yet')

        return delegate_dict
class Candidate:
    def __init__(self, name, stock_price_modifier):
        self.name = name
        self.delegates, self.popular_vote = -1
        self.shares = max_stocks_for_candidate
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

    def sell_candidate_stock(self):

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
        self.state_votes = {}

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

# def calculate_delegates_for_players(players, state):
#     state_name =

candidates_list = []
players = []

# To-Do: Need to refine logic and approach for 'results' component -LD
# iowa = State("Iowa", data.primary_dates["Iowa"])
# for candidate in data.candidates:
#     candidates_list.append(Candidate(candidate))
#
# results_for_2016 = {}

# results_for_2016['IOWA']
