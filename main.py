from agent import Agent
from interface.visualizer import run_visualizer
import time

# Graph 1: 10 vertices, 15 edges, 4 recharge stations
# Goal: reach vertex 10 (the last vertex) from vertex 1
agent = Agent(
    graphId="1",
    capacity=10,
    timePenalty=1,
    costPenalty=2,
    reachGoalReward=100
)

GAMMA = 0.9

def print_result(label, path, total_reward, elapsed):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Time: {elapsed:.4f}s | Steps: {len(path)} | Total reward: {total_reward:.2f}")
    print(f"  Path:")
    for i, step in enumerate(path, 1):
        print(f"    {i}. {step}")

# ─────────────────────────────────────────────
#  VALUE ITERATION (optimal baseline)
# ─────────────────────────────────────────────
start = time.time()
V = agent.valueIteration(gamma=GAMMA)
elapsed = time.time() - start
path, reward = agent.getPathFromV(V, gamma=GAMMA)
print_result("Value Iteration (optimal)", path, reward, elapsed)

# ─────────────────────────────────────────────
#  Q-LEARNING — parameter configurations
# ─────────────────────────────────────────────
configs = [
    {
        "label": "Q-Learning: low exploration (ε=0.3, decay=0.999)",
        "params": dict(gamma=GAMMA, alpha=0.1, episodes=50000, max_steps=500,
                       epsilon=0.3, epsilon_min=0.01, epsilon_decay=0.999),
    },
    {
        "label": "Q-Learning: medium exploration (ε=1.0, decay=0.9995)",
        "params": dict(gamma=GAMMA, alpha=0.1, episodes=50000, max_steps=500,
                       epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.9995),
    },
    {
        "label": "Q-Learning: high exploration (ε=1.0, decay=0.99999)",
        "params": dict(gamma=GAMMA, alpha=0.1, episodes=50000, max_steps=500,
                       epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.99999),
    },
    {
        "label": "Q-Learning: fast learning rate (α=0.5)",
        "params": dict(gamma=GAMMA, alpha=0.5, episodes=50000, max_steps=500,
                       epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.9995),
    },
    {
        "label": "Q-Learning: fewer episodes (10k)",
        "params": dict(gamma=GAMMA, alpha=0.1, episodes=10000, max_steps=500,
                       epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.999),
    },
]

results = []

# ─────────────────────────────────────────────
#  RUN Q-LEARNING CONFIGS
# ─────────────────────────────────────────────
for config in configs:
    start = time.time()

    Q, history = agent.Qlearning(**config["params"])

    elapsed = time.time() - start
    path, reward = agent.getPath(Q)

    print_result(config["label"], path, reward, elapsed)

    results.append({
        "label": config["label"],
        "steps": len(path),
        "reward": reward,
        "Q": Q,
        "history": history
    })


# ─────────────────────────────────────────────
#  SUMMARY TABLE
# ─────────────────────────────────────────────
print(f"\n\n{'='*60}")
print(f"  SUMMARY")
print(f"{'='*60}")
print(f"  {'Method':<48} {'Steps':>5} {'Reward':>8}")
print(f"  {'-'*48} {'-'*5} {'-'*8}")

# Value Iteration
V = agent.valueIteration(gamma=GAMMA)
vi_path, vi_reward = agent.getPathFromV(V, gamma=GAMMA)
print(f"  {'Value Iteration (optimal)':<48} {len(vi_path):>5} {vi_reward:>8.2f}")

# Q-learning results (sem rodar de novo)
for r in results:
    print(f"  {r['label']:<48} {r['steps']:>5} {r['reward']:>8.2f}")

print("\nEscolha qual configuração visualizar:\n")

for i, r in enumerate(results):
    print(f"{i} - {r['label']}")

choice = int(input("\nDigite o índice: "))

run_visualizer(agent, results[choice]["history"])
