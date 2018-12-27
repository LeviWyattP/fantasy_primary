import datetime
import data_stores as data
import primary_results as testdata

max_stocks_for_candidate = 10
class League:
    def __init__(self):
        self.players ={}
        self.player_names = self.players.keys()
        self.candidates = {}
        self.candidate_names = self.candidates.keys()
        self.states = {}

    def build_players(self, players, starting_money):
        for player in players:
            self.players[player] = Player(players, starting_money)
            print('building players')
        self.player_names = self.players.keys()
    def build_candidates(self, candidates, stock_price_modifiers):
        for candidate in candidates:
            self.candidates[candidate] = Candidate(candidate, stock_price_modifiers[candidate])
            print("building candidates")
        self.candidate_names = self.candidates.keys()
    def build_states(self):
        #Now we create states = this really should be a for loop for each state... but now just IOWA
        statename= 'Iowa'
        self.states[statename] = State(statename, data.primary_dates[statename][0], data.primary_dates[statename][1],{}, ['none'])
    def update_state_data(self, state_name, state_dict):
        self.states[state_name].update_results(state_dict)

        # update candidate info based on new data
        for candidate in self.candidate_names:


            self.candidates[candidate].update_candidate_data_from_state(state_name, state_dict[candidate][1],
                                                                        state_dict[candidate][0])
        # now we should update players based on new state data

        # first - clean up old player vote total for state
        self.states[state_name].total_player_votes = 0

        for player in self.player_names:
            player_votes = self.states[state_name].calculate_player_votes(self.players[player].stocks)
            self.players[player].set_player_votes_for_state(state_name, player_votes)

        # now we have total player votes in the state class - so we can do the delegate count
        for player in self.player_names:
            player_votes = self.players[player].state_votes[state_name]
            player_delegates = self.states[state_name].calculate_delegates_for_players(player_votes)
            self.players[player].set_player_delegates_for_state(state_name, player_delegates)
class State:

    def __init__(self, state, date_of_primary, state_delegates, results, unique_primaries):
        self.name = state
        self.primary_date = date_of_primary
        self.state_delegates = state_delegates
        self.results = results
        self.total_player_votes = 0

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
    def calculate_player_votes(self, player_stocks):

        votes = 0
        for each_candidate in player_stocks:

            # The percent vote share for the individual is the number of stocks they have divided by the total
            # possible stocks for candidates.
            percent_share = player_stocks[each_candidate] / max_stocks_for_candidate

            votes_for_candidate = self.results_dict[each_candidate][1] * percent_share

            votes = votes + votes_for_candidate
        return votes
    def calculate_delegates_for_players(self, player_votes):

        # generic proportional distribution
        if not self.primary_rules:
            if self.total_player_votes != 0:
                return(round(player_votes/self.total_player_votes))
            else:
                return 0

        # TODO does rounding work out and make the delegate counts consistent??

        else:
            # TODO write code for individual primary rules?
            print('I havent writte this could yet')

class Candidate:
    def __init__(self, name, stock_price_modifier):
        self.name = name
        self.delegates = -1
        self.popular_vote = -1
        self.shares = max_stocks_for_candidate
        self.stock_price_modifier = stock_price_modifier
        self.stock_price = 0
        self.set_stock_price()
        self.state_votes = {}
        self.state_delegates = {}
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
    def update_candidate_data_from_state(self, state_name, new_votes, new_delegates):

        # clean up before we add new data
        # TODO is there an error here where popular vote and total delegates are accidently subtracted more than once?
        if state_name in self.state_votes.keys() and self.state_votes[state_name] > 0:
            self.popular_vote = self.popular_vote - self.state_votes[state_name]
        if state_name in self.state_delegates.keys() and self.state_delegates[state_name] > 0:
            self.delegates = self.delegates - self.state_delegates[state_name]

        # now add the new data
        self.popular_vote += new_votes
        self.delegates += new_delegates

        self.state_votes[state_name] = new_votes
        self.state_delegates[state_name] = new_delegates


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.delegates = 0
        self.total_votes = 0

        # stocks. Key = name; result = number of stocks
        self.stocks = {}
        self.state_votes = {}
        self.state_delegates = {}
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
    def set_player_votes_for_state(self, state_name, player_votes):

        # first clean up any old votes
        if state_name in self.state_votes.keys() and self.state_votes[state_name] > 0:
            self.total_votes = self.total_votes - player_votes

        self.state_votes[state_name] = player_votes
        self.total_votes += player_votes
    def set_player_delegates_for_state(self, state_name, player_delegates):

        #first clean up any old votes
        if state_name in self.state_delegates.keys() and self.state_delegates[state_name] > 0:
            self.delegates = self.delegates - player_delegates
        self.state_delegates[state_name] = player_delegates
        self.delegates += player_delegates


# def create_league():
players = ['Levi', 'Lex', 'Eric']
league = League()
league.build_players(players, 20)
league.build_candidates(data.candidates, data.stock_price_modifiers)
league.build_states()
    # return league

# def update_data(league):
league.update_state_data("Iowa", testdata.iowa)

a =1

class stupid_dictionary_item_class:
    def __init__(self):
        self.ascii_key = 'kasich'
        self.memory_key = 0x085516
        value
# league = create_league()
# update_data(league)

# To-Do: Need to refine logic and approach for 'results' component -LD
# iowa = State("Iowa", data.primary_dates["Iowa"])
# for candidate in data.candidates:
#     candidates_list.append(Candidate(candidate))
#
# results_for_2016 = {}

# results_for_2016['IOWA']
