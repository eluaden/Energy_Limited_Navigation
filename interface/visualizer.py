import pygame
import math


WIDTH, HEIGHT = 1000, 720
NODE_RADIUS = 26

BACKGROUND = (238, 241, 245)
PANEL = (255, 255, 255)
TEXT = (25, 30, 40)

EDGE = (175, 180, 190)
NODE = (225, 228, 235)
NODE_BORDER = (45, 50, 60)

GOAL = (80, 210, 120)
RECHARGE = (90, 165, 255)
CURRENT = (255, 90, 90)
NEXT = (255, 185, 80)
ENERGY = (80, 190, 120)
ENERGY_BG = (220, 225, 230)


def decode_state(state_id, capacity):
    vertex = state_id // (capacity + 1)
    energy = state_id % (capacity + 1)
    return vertex, energy


def generate_circle_positions(num_vertices):
    cx, cy = WIDTH // 2 + 120, HEIGHT // 2
    radius = 260
    positions = {}

    for i in range(num_vertices):
        angle = 2 * math.pi * i / num_vertices - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions[i] = (int(x), int(y))

    return positions


def get_edges(agent):
    edges = set()
    capacity = agent.graphModeling.capacity

    for state in agent.states:
        curr_vertex, _ = decode_state(state.id, capacity)

        for next_state in state.neighborStates:
            next_vertex, _ = decode_state(next_state.id, capacity)

            if curr_vertex != next_vertex:
                edges.add(tuple(sorted((curr_vertex, next_vertex))))

    return list(edges)


def get_recharge_vertices(agent):
    recharge_vertices = set()
    capacity = agent.graphModeling.capacity

    for state in agent.states:
        curr_vertex, curr_energy = decode_state(state.id, capacity)

        for next_state in state.neighborStates:
            next_vertex, next_energy = decode_state(next_state.id, capacity)

            if curr_vertex == next_vertex and next_energy > curr_energy:
                recharge_vertices.add(curr_vertex)

    return recharge_vertices


def draw_rounded_rect(screen, rect, color, radius=16):
    pygame.draw.rect(screen, color, rect, border_radius=radius)


def draw_energy_bar(screen, font, x, y, width, height, energy, capacity):
    pygame.draw.rect(screen, ENERGY_BG, (x, y, width, height), border_radius=10)

    ratio = 0 if capacity == 0 else energy / capacity
    fill_width = int(width * ratio)

    if fill_width > 0:
        pygame.draw.rect(screen, ENERGY, (x, y, fill_width, height), border_radius=10)

    pygame.draw.rect(screen, (120, 130, 145), (x, y, width, height), 2, border_radius=10)

    label = font.render(f"Energy: {energy}/{capacity}", True, TEXT)
    screen.blit(label, (x, y - 30))


def draw_legend(screen, small_font, x, y):
    items = [
        ("Current", CURRENT),
        ("Next", NEXT),
        ("Goal", GOAL),
        ("Recharge", RECHARGE),
    ]

    for label, color in items:
        pygame.draw.circle(screen, color, (x, y), 9)
        text = small_font.render(label, True, TEXT)
        screen.blit(text, (x + 18, y - 10))
        y += 28


def draw_graph(
    screen,
    font,
    small_font,
    positions,
    edges,
    recharge_vertices,
    capacity,
    curr_vertex,
    curr_energy,
    next_vertex,
    next_energy,
    episode,
    step,
    reward,
    epsilon,
    speed
):
    screen.fill(BACKGROUND)

    # Left panel
    draw_rounded_rect(screen, (24, 24, 280, HEIGHT - 48), PANEL, 20)

    title = font.render("Q-Learning Replay", True, TEXT)
    screen.blit(title, (48, 48))

    action_text = "Recharge" if curr_vertex == next_vertex else "Move"
    action_color = RECHARGE if action_text == "Recharge" else NEXT

    lines = [
        f"Episode: {episode}",
        f"Step: {step}",
        f"Action: {action_text}",
        f"From: {curr_vertex + 1}",
        f"To: {next_vertex + 1}",
        f"Reward: {reward}",
        f"Epsilon: {epsilon:.4f}",
        f"Speed: {speed} FPS",
    ]

    y = 100
    for line in lines:
        text = small_font.render(line, True, TEXT)
        screen.blit(text, (48, y))
        y += 28

    pygame.draw.circle(screen, action_color, (235, 154), 10)

    draw_energy_bar(
        screen,
        small_font,
        48,
        360,
        210,
        24,
        next_energy,
        capacity
    )

    draw_legend(screen, small_font, 58, 445)

    controls = [
        "SPACE: pause/resume",
        "UP/DOWN: speed",
        "R: restart",
    ]

    y = HEIGHT - 135
    for control in controls:
        text = small_font.render(control, True, (80, 85, 95))
        screen.blit(text, (48, y))
        y += 26

    # Draw edges
    for u, v in edges:
        pygame.draw.line(screen, EDGE, positions[u], positions[v], 4)

    # Highlight current transition
    if curr_vertex != next_vertex:
        pygame.draw.line(
            screen,
            (255, 140, 60),
            positions[curr_vertex],
            positions[next_vertex],
            7
        )

    # Draw vertices
    for vertex, pos in positions.items():
        color = NODE
        radius = NODE_RADIUS

        if vertex in recharge_vertices:
            color = RECHARGE

        if vertex == len(positions) - 1:
            color = GOAL

        if vertex == next_vertex and next_vertex != curr_vertex:
            color = NEXT
            radius = NODE_RADIUS + 3

        if vertex == curr_vertex:
            color = CURRENT
            radius = NODE_RADIUS + 5

        pygame.draw.circle(screen, (210, 215, 225), (pos[0] + 3, pos[1] + 4), radius)
        pygame.draw.circle(screen, color, pos, radius)
        pygame.draw.circle(screen, NODE_BORDER, pos, radius, 2)

        label = font.render(str(vertex + 1), True, (0, 0, 0))
        rect = label.get_rect(center=pos)
        screen.blit(label, rect)

        if vertex in recharge_vertices:
            bolt = small_font.render("⚡", True, (255, 255, 255))
            screen.blit(bolt, (pos[0] - 8, pos[1] + radius - 6))

    pygame.display.flip()


def run_visualizer(agent, history):
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q-Learning Visualizer")

    font = pygame.font.SysFont("Arial", 22, bold=True)
    small_font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    capacity = agent.graphModeling.capacity

    num_vertices = max(
        decode_state(state.id, capacity)[0]
        for state in agent.states
    ) + 1

    positions = generate_circle_positions(num_vertices)
    edges = get_edges(agent)
    recharge_vertices = get_recharge_vertices(agent)

    running = True
    paused = False

    episode_index = 0
    step_index = 0
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_UP:
                    speed += 1

                elif event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)

                elif event.key == pygame.K_r:
                    episode_index = 0
                    step_index = 0
                    paused = False

        if not paused and episode_index < len(history):
            episode_data = history[episode_index]
            steps = episode_data["steps"]

            if step_index < len(steps):
                step_data = steps[step_index]

                draw_graph(
                    screen=screen,
                    font=font,
                    small_font=small_font,
                    positions=positions,
                    edges=edges,
                    recharge_vertices=recharge_vertices,
                    capacity=capacity,
                    curr_vertex=step_data["curr_vertex"],
                    curr_energy=step_data["curr_energy"],
                    next_vertex=step_data["next_vertex"],
                    next_energy=step_data["next_energy"],
                    episode=episode_data["episode"],
                    step=step_data["step"],
                    reward=step_data["reward"],
                    epsilon=step_data["epsilon"],
                    speed=speed
                )

                step_index += 1

            else:
                episode_index += 1
                step_index = 0

        clock.tick(speed)

    pygame.quit()