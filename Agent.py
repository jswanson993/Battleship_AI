import random
import collections

class QLearningAgent:

    def __init__(self, lr=.5, discount=.5, exploration=.5):
        self.QVals = collections.Counter()
        self.lr = lr
        self.discount = discount
        self.exploration = exploration

    def getQValue(self, state, action):
        """
        Should return Q(state, action)
        """

        val = self.QVals[(''.join(map(str, state)), action)]

        if val is not None:
            return val
        else:
            return 0.0

    def computeMaxValueFromQValues(self, state):
        maxVal = float("-inf")
        if len(self.getLegalActions(state)) == 0:
            return 0.0

        for action in self.getLegalActions(state):
            maxVal = max(maxVal, self.getQValue(state, action))

        return maxVal

    def updateQValue(self, state, action, reward):
        self.QVals[(''.join(map(str, state)), action)] = (1 - self.lr) * self.getQValue(state, action) + self.lr * \
                                      (reward + self.discount * self.computeMaxValueFromQValues(state))

    def getLegalActions(self, state):
        actions = []
        for i in range(0, 10):
            for j in range (0, 10):
                if state[j][i] == 0:
                    actions.append((i, j))
        return actions

    def takeAction(self, state):
        best_action = (0, 0)
        best_val = float("-inf")
        legal_actions = self.getLegalActions(state)
        for action in legal_actions:
            max_val = max(best_val, self.getQValue(state, action))
            if max_val > best_val:
                best_action = action
                best_val = max_val

        #if random.uniform(0, 1) < self.exploration:
        #    best_action = (random.randrange(0, 9), random.randrange(0, 9))
        #    while not legal_actions.__contains__(best_action):
        #        best_action = (random.randrange(0, 9), random.randrange(0, 9))

        return best_action[0], best_action[1]
