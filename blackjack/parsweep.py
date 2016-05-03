
# coding: utf-8

# In[7]:

import blackjacktools as bj
import matplotlib.pyplot as plt

M = 150
Hmax = 500
Lmin = 50
for H in range(M,Hmax,5):
    for L in range(Lmin,M,5):
        table = bj.Table()
        table.shuffle_deck(n=6)
        table.set_players([bj.Player(L,H,bank_roll = 5000) for _ in range(5)])
        bal = table.run(max_hands = 800)
        plt.title("{} {}".format(L,H))
        plt.plot(bal.T)
        plt.ylim((0,25000))
        plt.savefig("img/{}_{}.pdf".format(L,H))
        plt.clf()

