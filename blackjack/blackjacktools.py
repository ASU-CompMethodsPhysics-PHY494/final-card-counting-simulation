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
    
    def compute_gains(self,bank_roll,small_bet,med_bet,large_bet):
        money = self.bank_roll   #Start out with this much money per player, can change this from zero whenever
        if self.get_count() < 3 and player_win is True:
            money += small_bet
        elif self.get_count() < 3 and player_win is False:
            money -= small_bet()
        elif 3 < self.get_count() < 10 and player_win is True:
            money += med_bet
        elif 3 < self.get_count() < 10 and player_win is False:
            money -= small_bet
        elif self.get_count() > 10 and player_win is True:
            money += large_bet
        else:
            money -= large_bet

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
    def __init__(self):
        super(Player,self).__init__()
        
class Dealer(Agent):
    def __init__(self):
        super(Dealer,self).__init__()
    