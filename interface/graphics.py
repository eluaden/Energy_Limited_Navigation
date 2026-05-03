import os
import json
import matplotlib.pyplot as plt
import numpy as np


# =========================
# Utils
# =========================

def ensure_dir(graph_id, config_name):
    path = f"outputs/graph_{graph_id}/{config_name}"
    os.makedirs(path, exist_ok=True)
    return path


def save_config(path, config):
    with open(f"{path}/config.json", "w") as f:
        json.dump(config, f, indent=4)


# =========================
# 1. Reward por episódio
# =========================

def plot_rewards(history, path):
    episodes = [h["episode"] for h in history]
    rewards = [h["total_reward"] for h in history]

    plt.figure()
    plt.plot(episodes, rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Reward per Episode")
    plt.grid()
    plt.savefig(f"{path}/rewards.png")
    plt.close()


# =========================
# 2. Passos por episódio
# =========================

def plot_steps(history, path):
    episodes = [h["episode"] for h in history]
    steps = [h["num_steps"] for h in history]

    plt.figure()
    plt.plot(episodes, steps)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.title("Steps per Episode")
    plt.grid()
    plt.savefig(f"{path}/steps.png")
    plt.close()




def plot_epsilon(history, path):
    episodes = [h["episode"] for h in history]
    eps = [h["epsilon"] for h in history]

    plt.figure()
    plt.plot(episodes, eps)
    plt.xlabel("Episode")
    plt.ylabel("Epsilon")
    plt.title("Exploration Decay")
    plt.grid()
    plt.savefig(f"{path}/epsilon.png")
    plt.close()


# =========================
# 5. TD Error médio
# =========================

def plot_td_error(history, path):
    episodes = [h["episode"] for h in history]
    errors = [h["avg_td_error"] for h in history]

    plt.figure()
    plt.plot(episodes, errors)
    plt.xlabel("Episode")
    plt.ylabel("Avg TD Error")
    plt.title("TD Error over Time")
    plt.grid()
    plt.savefig(f"{path}/td_error.png")
    plt.close()


# =========================
# 6. Heatmap de visita
# =========================

# =========================
# 7. Curva de aprendizado (suavizada)
# =========================

def plot_smoothed_rewards(history, path, window=10):
    rewards = [h["total_reward"] for h in history]

    smoothed = []
    for i in range(len(rewards)):
        start = max(0, i - window)
        smoothed.append(np.mean(rewards[start:i+1]))

    plt.figure()
    plt.plot(smoothed)
    plt.xlabel("Episode")
    plt.ylabel("Smoothed Reward")
    plt.title("Learning Curve (Smoothed)")
    plt.grid()
    plt.savefig(f"{path}/smoothed_rewards.png")
    plt.close()


# =========================
# Função principal
# =========================

def generate_all(history, num_vertices, graph_id, config_name, config_dict=None):
    path = ensure_dir(graph_id, config_name)

    if config_dict:
        save_config(path, config_dict)

    plot_rewards(history, path)
    plot_smoothed_rewards(history, path)
    plot_steps(history, path)
    plot_epsilon(history, path)
    plot_td_error(history, path)

    print(f"[OK] Gráficos salvos em: {path}")