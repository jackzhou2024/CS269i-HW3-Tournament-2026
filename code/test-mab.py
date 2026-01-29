# An example that shows how to use the UCB1 learning policy
# to make decisions between two arms based on their expected rewards.

# Import MABWiser Library
from mabwiser.mab import MAB, LearningPolicy, NeighborhoodPolicy

# Data
arms = ['Arm1', 'Arm2']
decisions = ['Arm1', 'Arm1', 'Arm2', 'Arm1']
rewards = [20, 17, 25, 9]

# Model
mab = MAB(arms, LearningPolicy.UCB1(alpha=1.25))

# Train
mab.fit(decisions, rewards)

# Add data
added_decisions = ['Arm1', 'Arm2']
added_rewards = [1, 2]

mab.partial_fit(added_decisions, added_rewards)

# Test
p = mab.predict()
print(p)
