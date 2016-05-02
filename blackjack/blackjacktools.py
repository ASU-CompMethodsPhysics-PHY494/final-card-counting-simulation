import random
import numpy as np

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
            return Card(None,None)
        return self.cards.pop(random.randrange(0,len(self.cards)))

    def summary(self):
        out = "Number of Cards: {}\n".format(self.__len__())
        for c in self.cards:
            out += "{} of {}\n".format(c.rank,c.suit)
        return out[:-1] #strip last new line

    def __len__(self):
        return len(self.cards)
    
deck = Deck()    
deck.shuffle()
    
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
        return count
    
    def set_balance(self,new_balance):
        self.bank_roll = new_balance
    
    def get_balance(self):
        return self.bank_roll

    def hit(self, deck):
        self.add_card(deck.deal())   #Add a card to the player's hand
    
    def auto_move(self, deck):           #Implemented a basic version, still need to add the card counting rules
        while self.get_score() <= 21:
            if 16 < self.get_score() < 21:   #If player's score is between 16 and 21, the player stays and program prints cards/score
                break
            elif self.get_score() == 21:     #If player gets blackjack, output "Blackjack!" and break the loop
                break
            elif self.get_score() > 21:     #If player's score is greater than 21 off the bat (for error-proofing), break the loop
                break
            else:               #If player's score is less than 17, the player hits until one of the other criterias is met
                self.hit(deck)
                if self.get_score() == 21:    #If player hits to 21, print the message and break the loop
                    break
        return self.get_score()
             
class Player(Agent):
    def __init__(self,small_bet,large_bet,bank_roll=5000):
        super(Player,self).__init__()
        self.small_bet = small_bet
        self.large_bet = large_bet
        self.med_bet = .5*(small_bet + large_bet)
        self.bank_roll = bank_roll
       
        
    def compute_gains(self,count, table):
        #if neither the player or dealer wins, the player doesn'y gain or lose any money. 
        
        small_bet = self.small_bet
        med_bet = self.med_bet
        large_bet = self.large_bet
        
        winner = table.pvd(self)
        if winner is None:
            #print("Nobody fucking won")
            pass
            
        #The following tells the player how to bet. Given the count, the player bets a set amount of money. It is intuitively obious to the casual observer that they get the money back if they win, and lose the money if they don't.
        else:
            if winner is self:
                if count < -1:
                    self.bank_roll += small_bet
                if (-1 <= count) and (count <= 1):
                    self.bank_roll += med_bet
                if count > 1: 
                    self.bank_roll += large_bet
            if winner is not self and winner is not None:
                if count < -1:
                    self.bank_roll -= small_bet
                if (-1 <= count) and (count <= 1):
                    self.bank_roll -= med_bet
                if count > 1: 
                    self.bank_roll -= large_bet
        
class Dealer(Agent):
    def __init__(self):
        super(Dealer,self).__init__()
        
class Table(object):
    def __init__(self):
        self.P = []
        self.D = Dealer()
        self.deck = Deck()
        self.num_decks = None
        self.current_count = None
        
    def shuffle_deck(self,n=3):
        self.current_count = 0
        self.num_decks = n
        self.deck.shuffle(n=n)
        
    def set_players(self,players):
        self.P = players
        
    def pvd(self, player):
        #Defines win/loss, player is returned if player wins, dealer is returned if player loses
        if player.get_score() == 21:
            if len(player.hand) == 2:
                return player
            if len(player.hand) > 2:
                if self.D.get_score() < 21:
                    return player
        if player.get_score() == self.D.get_score():
            return None
        if player.get_score() > 21:
            return self.D
        if self.D.get_score() > 21 and player.get_score() <= 21: 
            return player
        if player.get_score() < 21 and self.D.get_score() < 21:
            if self.D.get_score() < player.get_score():
                return self.D
            else: 
                return player
    def run(self,max_hands=800):
        ### RUN SIMULATION HERE
        balances = np.zeros((len(self.P),max_hands))
        player_status = np.array([True for _ in range(len(self.P))])
        for N in range(max_hands):
            #print('{}\r'.format(N))
            previous_count = self.current_count
            if any(player_status):
                for i, p in enumerate(self.P):
                    [p.add_card(self.deck.deal()) for _ in range(2)]
                    p.auto_move(self.deck)
                [self.D.add_card(self.deck.deal()) for _ in range(2)]
                self.D.auto_move(self.deck)   
                num_deck = (len(self.deck)//52)+1  
                # For loop through players to determine new balances (example below)
                for i,p in enumerate(self.P):
                    p.compute_gains(previous_count, self)
                    balances[i,N] = p.get_balance()
                    if p.bank_roll <=0:
                        player_status[i] = False
                    self.current_count += p.get_count()//num_deck
                self.current_count += self.D.get_count()//num_deck
                if len(self.deck) < 21:
                    self.shuffle_deck()
            [x.clear_hand() for x in self.P + [self.D]]
        return balances
                
                    
                
            