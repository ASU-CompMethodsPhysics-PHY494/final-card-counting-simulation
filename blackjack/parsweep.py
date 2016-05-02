
# coding: utf-8

# In[7]:

import blackjacktools as bj
import matplotlib.pyplot as plt



# In[10]:

M = 100
Hmax = 105
Lmin = 95
for H in range(M,Hmax):
    for L in range(Lmin,M):
        table = bj.Table()
        table.shuffle_deck(n=6)
        table.set_players([bj.Player(L,H,bank_roll = 5000) for _ in range(5)])
        bal = table.run(max_hands = 10)
        plt.title("{} {}".format(L,H))
        plt.plot(bal.T)
        plt.show()


# In[ ]:



