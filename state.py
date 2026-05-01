class State:
    def __init__(self, id):
        self.id = id
        self.neighborStates = []
        self.neighborRewards = []
    
    def addNeighbor(self, neighborState, reward):
        self.neighborStates.append(neighborState)
        self.neighborRewards.append(reward)
    