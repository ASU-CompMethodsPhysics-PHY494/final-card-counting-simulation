import random

class Card(object):
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def info(self):
        return (self.rank,self.suit)

    def __str__(self):
        return "{} of {}".format(self.rank,self.suit)

class Deck(object):
    def __init__(self):
        self.cards = []
    
    def shuffle(self,n=3):
        self.cards = []
        for _ in range(n):
            for x in list(range(2,11)) + [10,10,10,"Ace"]:
                for y in ["Clubs","Spades","Hearts","Diamonds"]:
                    self.cards.append(Card(x,y))

    def add_card(self,cards):
        if type(cards) is list:
            for card in cards:
                self.cards.append(card)
        else:
            self.cards.append(card)
    def deal(self):
        if self.__len__() == 0:
            print("Deck is empty!")
            return Card(None,None)
        return self.cards.pop(random.randrange(0,len(self.cards)))

    def summary(self):
        out = "Number of Cards: {}\n".format(self.__len__())
        for c in self.cards:
            out += "{} of {}\n".format(c.rank,c.suit)
        return out[:-1] #strip last new line

    def __len__(self):
        return len(self.cards)
    
class Agent(object):
    def __init__(self):
        self.hand = []
    def add_card(self,card):
        self.hand.append(card)
    def clear_hand(self):
        self.hand = []
    def get_score(self):
        score = 0
        aces = []
        for c in self.hand:
            if type(c.rank) is int:
                score += c.rank
            else:
                aces.append(c)
        for a in aces:
            if (score + 11) > 21:
                score += 1
            else:
                score += 11
        return score 
    def get_count(self):
        count = 0
        for c in self.hand:
            if type(c.rank) is int:
                if c.rank < 7:
                    count += 1
                elif c.rank is 7:
                    count += 0
                elif c.rank is 8:
                    count += 0
                elif c.rank is 9:
                    count += 0
                else:
                    count += -1
            else:
                count += -1
             
            
        return count
    
             
class Player(Agent):
    def __init__(self):
        super(Player,self).__init__()
        
class Dealer(Agent):
    def __init__(self):
        super(Dealer,self).__init__()
    