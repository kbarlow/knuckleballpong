
import pygame
import sys
import random
import math
import numpy as np
import os


# --- Q-learning Pong AI with Save/Load and Selection Screen ---
# State: (ball_y_bin, ball_vy_bin, paddle_y_bin)
# Actions: [up, down, stay]

pygame.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong ML')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 30, 150
BALL_SIZE = 20


# Discretization bins
def discretize(val, minv, maxv, bins):
    val = max(minv, min(maxv, val))
    return int((val - minv) / (maxv - minv + 1e-5) * (bins - 1))

N_BINS = 12
Q_FILE = "qtable.npy"

alpha = 0.2  # learning rate
gamma = 0.95 # discount
epsilon = 0.15 # exploration
ball_speed = 7
font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()

def load_qtable():
    if os.path.exists(Q_FILE):
        return np.load(Q_FILE)
    return np.zeros((N_BINS, N_BINS, N_BINS, 3))

def save_qtable(Q):
    np.save(Q_FILE, Q)

def reset_game_objects():
    left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    return left_paddle, right_paddle, ball

def reset_ball(ball):
    global ball_vx, ball_vy
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_vx = random.choice([-1, 1]) * ball_speed
    ball_vy = random.uniform(-1, 1) * ball_speed

def get_state(ball, right_paddle, left_paddle):
    by = discretize(ball.centery, 0, HEIGHT, N_BINS)
    bvy = discretize(ball_vy, -ball_speed, ball_speed, N_BINS)
    py = discretize(right_paddle.centery, 0, HEIGHT, N_BINS)
    ly = discretize(left_paddle.centery, 0, HEIGHT, N_BINS)
    return (by, bvy, py, ly)

def choose_action(Q, state):
    if random.random() < epsilon:
        return random.randint(0, 2)
    return int(np.argmax(Q[state]))

def step(action, right_paddle):
    if action == 0 and right_paddle.top > 0:
        right_paddle.y -= 12
    elif action == 1 and right_paddle.bottom < HEIGHT:
        right_paddle.y += 12

N_BINS = 12
Q_FILE = "qtable.npy"

def load_qtable():
    if os.path.exists(Q_FILE):
        return np.load(Q_FILE)
    return np.zeros((N_BINS, N_BINS, N_BINS, N_BINS, 3))

N_BINS = 12
def selection_screen(font):
    options = ["Continue Learning", "Restart Learning"]
    selected = 0
    while True:
        screen.fill(BLACK)
        title = font.render("Pong ML", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        for i, opt in enumerate(options):
            color = (200, 200, 0) if i == selected else WHITE
            text = font.render(opt, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i*100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    selected = (selected - 1) % len(options)
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return selected

# --- Main ---
while True:
    choice = selection_screen(font)
    if choice == 0 and os.path.exists(Q_FILE):
        Q = load_qtable()
    else:
        Q = np.zeros((N_BINS, N_BINS, N_BINS, N_BINS, 3))
        if os.path.exists(Q_FILE):
            os.remove(Q_FILE)
    left_paddle, right_paddle, ball = reset_game_objects()
    left_score = 0
    right_score = 0
    prev_state = None
    prev_action = None
    reset_ball(ball)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_qtable(Q)
                pygame.quit()
                sys.exit()
        # Human left paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= 12
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += 12
        # Q-learning AI for right paddle
        state = get_state(ball, right_paddle, left_paddle)
        action = choose_action(Q, state)
        step(action, right_paddle)
        # Move ball
        ball.x += int(ball_vx)
        ball.y += int(ball_vy)
        # Ball collision with top/bottom
        if ball.top < 0 or ball.bottom > HEIGHT:
            ball_vy *= -1
        # Ball collision with paddles
        reward = 0
        if ball.colliderect(left_paddle):
            ball.left = left_paddle.right
            ball_vx *= -1
        if ball.colliderect(right_paddle):
            ball.right = right_paddle.left
            ball_vx *= -1
            reward = 1
        # Ball out of bounds
        if ball.left <= 0:
            right_score += 1
            reward = 2
            reset_ball(ball)
        elif ball.right >= WIDTH:
            left_score += 1
            reward = -2
            reset_ball(ball)
        # Q-learning update
        if prev_state is not None and prev_action is not None:
            Q[prev_state][prev_action] += alpha * (reward + gamma * np.max(Q[state]) - Q[prev_state][prev_action])
        prev_state = state
        prev_action = action
        # Draw
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH//4, 20))
        screen.blit(right_text, (WIDTH*3//4, 20))
        pygame.display.flip()
        clock.tick(60)
