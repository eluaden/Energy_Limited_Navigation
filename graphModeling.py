from state import State

class GraphModeling:
    def __init__(self, path, capacity, timePenalty, costPenalty, reachGoalReward):
        self.path = path
        self.capacity = capacity
        self.timePenalty = timePenalty
        self.costPenalty = costPenalty
        self.reachGoalReward = reachGoalReward

    def vertexId(self, vertex, energy):
        return vertex * (self.capacity + 1) + energy

    def createStates(self):
        states = []
        with open(self.path) as f:
            linhas = f.readlines()
            
            n, m = map(int, linhas[0].strip().split())

            for i in range(n):
                for j in range(self.capacity + 1):
                    states.append(State(self.vertexId(i, j)))
            
            for i in range(1, m + 1):
                u, v, d = map(int, linhas[i].strip().split())
                u -= 1
                v -= 1
                for j in range(d, self.capacity + 1):
                    for _ in range(2):
                        if u == n - 1:
                            continue
                        
                        if v != n - 1:
                            states[self.vertexId(u, j)].addNeighbor(states[self.vertexId(v, j - d)], -self.timePenalty * d)
                        else:
                            states[self.vertexId(u, j)].addNeighbor(states[self.vertexId(v, j - d)], self.reachGoalReward - (self.timePenalty * d))
                        u, v = v, u
            
            p = int(linhas[m + 1].strip())
            for i in range(m + 2, m + 2 + p):
                v, c = map(int, linhas[i].strip().split())

                if v == n:
                    continue

                v -= 1
                for j in range(self.capacity):
                    states[self.vertexId(v, j)].addNeighbor(states[self.vertexId(v, j + 1)], -self.costPenalty * c)

        return states