from state import State
from graphModeling import GraphModeling
import os
import random

class Agent:
    def __init__(self, graphId, capacity, timePenalty, costPenalty, reachGoalReward):
        self.graphModeling = GraphModeling("graphs"+ os.sep + "grafo" + graphId + ".txt", capacity, timePenalty, costPenalty, reachGoalReward)
        self.states = self.graphModeling.createStates()
    
    def valueIteration(self, gamma, epsilon = 1e-6):
        V = [0] * len(self.states)
        while True:
            delta = 0
            for state in self.states:
                if not state.neighborStates:
                    continue
                v = V[state.id]
                V[state.id] = max([reward + (gamma * V[neighborState.id]) for neighborState, reward in zip(state.neighborStates, state.neighborRewards)])
                delta = max(delta, abs(v - V[state.id]))
            if delta < epsilon:
                break
        return V
    
    def Qlearning(self, gamma, alpha, episodes, max_steps=100, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        Q = [[0.0] * len(st.neighborStates) for st in self.states]

        for _ in range(episodes):
            state = self.states[0]
            step = 0

            while state.neighborStates and step < max_steps:
                step += 1
                if random.random() < epsilon:
                    actionIndex = random.randint(0, len(state.neighborStates) - 1)
                else:
                    actionIndex = 0
                    for i in range(1, len(state.neighborStates)):
                        if Q[state.id][i] > Q[state.id][actionIndex]:
                            actionIndex = i

                nextState = state.neighborStates[actionIndex]
                reward = state.neighborRewards[actionIndex]

                best_next_q = max(Q[nextState.id]) if Q[nextState.id] else 0.0
                Q[state.id][actionIndex] += alpha * (reward + (gamma * best_next_q) - Q[state.id][actionIndex])

                state = nextState

            epsilon = max(epsilon_min, epsilon * epsilon_decay)

        return Q

    def getPath(self, Q):
        """
        Follow the greedy policy from the Q-table and return the path taken.

        Returns a list of step descriptions, each being either:
          - "Traversed edge: vertex X -> vertex Y (energy: E1 -> E2)"
          - "Recharged at vertex X (energy: E1 -> E2)"
        Vertices are reported as 1-based indices.
        """
        capacity = self.graphModeling.capacity
        path = []
        state = self.states[0]
        total_reward = 0.0

        visited = set()

        while state.neighborStates:
            if state.id in visited:
                path.append("Cycle detected, stopping.")
                break
            visited.add(state.id)

            actionIndex = 0
            for i in range(1, len(state.neighborStates)):
                if Q[state.id][i] > Q[state.id][actionIndex]:
                    actionIndex = i

            nextState = state.neighborStates[actionIndex]
            total_reward += state.neighborRewards[actionIndex]

            path.append(self._describeStep(state, nextState, capacity))
            state = nextState

        return path, total_reward

    def getPathFromV(self, V, gamma):
        """
        Follow the optimal policy derived from the value function V.

        At each state, picks the action maximizing: reward + gamma * V[nextState].
        Returns the same format as getPath.
        """
        capacity = self.graphModeling.capacity
        path = []
        state = self.states[0]
        total_reward = 0.0

        visited = set()

        while state.neighborStates:
            if state.id in visited:
                path.append("Cycle detected, stopping.")
                break
            visited.add(state.id)

            bestValue = float('-inf')
            bestIndex = 0
            for i, (neighbor, reward) in enumerate(zip(state.neighborStates, state.neighborRewards)):
                value = reward + gamma * V[neighbor.id]
                if value > bestValue:
                    bestValue = value
                    bestIndex = i

            nextState = state.neighborStates[bestIndex]
            total_reward += state.neighborRewards[bestIndex]

            path.append(self._describeStep(state, nextState, capacity))
            state = nextState

        return path, total_reward

    def _describeStep(self, state, nextState, capacity):
        curr_vertex = state.id // (capacity + 1)
        curr_energy = state.id % (capacity + 1)
        next_vertex = nextState.id // (capacity + 1)
        next_energy = nextState.id % (capacity + 1)

        if curr_vertex == next_vertex:
            return f"Recharged at vertex {curr_vertex + 1} (energy: {curr_energy} -> {next_energy})"
        else:
            return f"Traversed edge: vertex {curr_vertex + 1} -> vertex {next_vertex + 1} (energy: {curr_energy} -> {next_energy})"