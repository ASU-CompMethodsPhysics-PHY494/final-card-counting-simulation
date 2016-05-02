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
    
deck = Deck()    
deck.shuffle()
    
class Agent(object):
    def __init__(self):
        self.hand = []
        
    def add_card(self,card):
        self.hand.append(card)
        
    def clear_hand(self):
        self.hand = []
        
    def get_hand(self):
        for n in range(2): 
            card = deck.deal()
            self.add_card(card)
        print([c.info() for c in self.hand])
        
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

    def hit(self):        #Finished!
        card = deck.deal()    #Create a local "card" object
        self.add_card(card)   #Add a card to the player's hand
        self.get_score()      #Retrieve the player's score
        if self.get_score() > 21:
            print("Player chose to hit but... Bust!")
            print([c.info() for c in self.hand])
        else:
            print("Player chose to hit!")
            print([c.info() for c in self.hand])
        return self.get_score()
                    
    def stay(self):        #Finished!
        print("Player chose to stay!")
        return self.get_score()
    
    def auto_move(self):           #Implemented a basic version, still need to add the card counting rules
        print(self.get_score())
        while self.get_score() <= 21:
            if 16 < self.get_score() < 21:   #If player's score is between 16 and 21, the player stays and program prints cards/score
                self.stay()
                print([c.info() for c in self.hand])
                break
            elif self.get_score() == 21:     #If player gets blackjack, output "Blackjack!" and break the loop
                print("Blackjack!")
                print([c.info() for c in self.hand])
                break
            elif self.get_score() > 21:     #If player's score is greater than 21 off the bat (for error-proofing), break the loop
                print("Ummm something went wrong...")
                break
            else:               #If player's score is less than 17, the player hits until one of the other criterias is met
                self.hit()
                if self.get_score() == 21:    #If player hits to 21, print the message and break the loop
                    print("Player gets 21!")
                    print([c.info() for c in self.hand])
                    print(self.get_score())
                    break
        return self.get_score()
             
class Player(Agent):
    def __init__(self,small_bet,large_bet):
        super(Player,self).__init__()
        self.small_bet = small_bet
        self.large_bet = large_bet
       
        
    def compute_gains(self,count):
        money = self.bank_roll   #Start out with this much money per player, can change this from zero whenever
        
        #if neither the player or dealer wins, the player doesn'y gain or lose any money. 
        
        winner = Table.pvd(self)
        
        if winner is None:
            pass
            
        #The following tells the player how to bet. Given the count, the player bets a set amount of money. It is intuitively obious to the casual observer that they get the money back if they win, and lose the money if they don't.
        else:
            if winner is self:
                if count < -1:
                    money += small_bet
                if (-1 <= count) and (count <= 1):
                    money += med_bet
                if count > 1: 
                    money += large_bet
            if winner is not self and winner is not None:
                if count < -1:
                    money -= small_bet
                if (-1 <= count) and (count <= 1):
                    money -= med_bet
                if count > 1: 
                    money -= large_bet
        
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
            if len(player.get_hand()) == 2:
                return player
            if len(player.get_hand()) > 2:
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
            previous_count = self.current_count
            if any(player_status):
                deck.deal()
                players.auto_move
                self.D.auto_move
                num_deck = len(self.deck)//52    
                # For loop through players to determine new balances (example below)
                for i,p in enumerate(self.P):
                    p.compute_gains(previous_count)
                    balances[i,N] = p.get_balance()
                    if self.bank_roll <=0:
                        player_status[i] = False
                    self.current_count += p.get_count()//num_deck
                self.current_count += self.D.get_count()//num_deck
                if len(self.deck) < 21:
                    Table.shuffle_deck()
                
                    
                
            