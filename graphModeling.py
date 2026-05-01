from state import State

class GraphModeling:
    def __init__(self, path, capacity, timePenalty, costPenalty):
        self.path = path
        self.capacity = capacity
        self.timePenalty = timePenalty
        self.costPenalty = costPenalty

    def createStates(self):
        states = []
        with open(self.path) as f:
            linhas = f.readlines()
            
            n, m = map(int, linhas[0].strip().split())

            for i in range(n):
                for j in range(self.capacity + 1):
                    states.append(State(i * n + j))
            
            for i in range(1, m + 1):
                u, v, d = map(int, linhas[i].strip().split())
                u -= 1
                v -= 1
                for j in range(d, self.capacity + 1):
                    states[u * n + j].addNeighbor(states[v * n + (j - d)], self.timePenalty * d)
            
            p = int(linhas[m + 1].strip())
            for i in range(m + 2, m + 2 + p):
                v, c = map(int, linhas[i].strip().split())
                v -= 1
                for j in range(self.capacity):
                    states[v * n + j].addNeighbor(states[v * n + (j + 1)], self.costPenalty * c)
                    
        return states