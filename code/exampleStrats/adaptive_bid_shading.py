import numpy as np


# value is your private value in this round.
# totalValue is your total value so far.
# totalPayment is your total spending so far.
# ROI is your ROI constraint in this auction, ROI is constant over 10,000 rounds.
# We also provide the history for you
# During round n, you receive the history for the past (n-1) rounds, i.e.,
# The length of myHistory is n-1
# myHistory[i] is a 4-element list, including 
# (0) your private value in round i
# (1) your bid price in round i
# (2) your allocation result (whether or not you got the item, 1 - yes, 0 - no) in round i
# (3) your payment in round i

EPS = 0.05 # learning rate
mu = 0 # shading factor

# return the pseudonym of your strategy
def get_name():
    return "adaptive_bid_shading"

def update_pacing_factor(totalValue, totalPayment,  ROI):
    global mu
    ratio = 100
    if (totalPayment > 0):
        ratio = totalValue / totalPayment 
    mu += EPS * (ROI + 0.1 - ratio)
    mu = max(0, mu)

def strategy(value, totalValue, totalPayment, ROI, myHistory):
    global mu
    if (len(myHistory) > 0):
        update_pacing_factor(totalValue, totalPayment, ROI)
    else:
        mu = 0
    return value / (mu + 1)
