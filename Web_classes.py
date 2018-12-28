__author__ = 'Levi'


class Web_Player:

    def __init__(self, name, votes, delegates):
        self.name = name
        self.votes = votes
        self.delegates = delegates
        self.profile_picture = r'C:\Users\Levi\PycharmProjects\fantasy_primary\static\lex_pic.jpg'


class Web_Candidate:

    def __init__(self, name, votes, delegates):
        self.name = name
        self.votes = votes
        self.delegates = delegates

class Primary_Table:

    def __init__(self, date, state, delegates):
        # TODO date needs to be updated so it is sortable in the table - lex can you do this?
        self.date = date
        self.state =  state
        self.delegates = delegates
