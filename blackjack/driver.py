import blackjacktools as bj
import matplotlib.pyplot as plt

pri = 1000
s = 50
l = 150
hands = 10000
decks = 6

table = bj.Table()
table.set_players([bj.Player(s,l,bank_roll=pri) for _ in range(5)])
table.shuffle_deck(n=decks)
bal = table.run(max_hands=hands)
plt.plot(bal.T)
plt.plot([x for x in range(len(bal[0]))],[pri for x in range(len(bal[0]))],'r--')
plt.plot([x for x in range(len(bal[0]))],[0 for x in range(len(bal[0]))],'b--')
plt.show()
