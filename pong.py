import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 30, 150
PADDLE_ACC = 0.49  # 30% slower acceleration
PADDLE_FRICTION = 0.29  # 30% slower friction
PADDLE_MAX_SPEED = 4.9   # 30% slower max speed for paddles

# Ball settings
BALL_SIZE = 20
BALL_SPEED = 1.7  # 30% slower initial speed
BALL_MAX_SPEED = 7.8  # 30% slower max speed for the ball
BALL_ANGLE = math.radians(0)  # Start moving horizontally
BALL_SPEED_X = BALL_SPEED * math.cos(BALL_ANGLE)
BALL_SPEED_Y = BALL_SPEED * math.sin(BALL_ANGLE)
BALL_SPIN = 0.0  # Spin value, positive = curve down, negative = curve up
SPIN_DECAY = 0.96  # 30% slower decay
SPIN_EFFECT = 0.12  # 30% less spin effect


# Paddles
left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
left_vel = [0.0, 0.0]  # [vx, vy]
right_vel = [0.0, 0.0]
# Paddle acceleration trackers (scalar, not vector)
left_accel = 0.0
right_accel = 0.0
PADDLE_ACCEL_MAX = 4.9
PADDLE_ACCEL_INC = 0.49
PADDLE_ACCEL_DECAY = 0.34

# Ball
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Scores
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

last_hit = None  # Track which paddle last hit the ball
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Paddle movement with velocity and acceleration
    keys = pygame.key.get_pressed()
    # Left paddle acceleration and acceleration tracking
    left_moving = False
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_vel[1] -= PADDLE_ACC
        left_moving = True
    elif keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_vel[1] += PADDLE_ACC
        left_moving = True
    else:
        if left_vel[1] > 0:
            left_vel[1] -= PADDLE_FRICTION
            if left_vel[1] < 0:
                left_vel[1] = 0
        elif left_vel[1] < 0:
            left_vel[1] += PADDLE_FRICTION
            if left_vel[1] > 0:
                left_vel[1] = 0
    if keys[pygame.K_a] and left_paddle.left > 0:
        # Prevent left paddle from crossing the ball
        if left_paddle.right - left_vel[0] > ball.left and left_paddle.bottom > ball.top and left_paddle.top < ball.bottom:
            left_paddle.x = ball.left - PADDLE_WIDTH
            left_vel[0] = 0
        else:
            left_vel[0] -= PADDLE_ACC
            left_moving = True
    elif keys[pygame.K_d] and left_paddle.right < WIDTH//2:
        if left_paddle.right + left_vel[0] > ball.left and left_paddle.bottom > ball.top and left_paddle.top < ball.bottom:
            left_paddle.x = ball.left - PADDLE_WIDTH
            left_vel[0] = 0
        else:
            left_vel[0] += PADDLE_ACC
            left_moving = True
    else:
        if left_vel[0] > 0:
            left_vel[0] -= PADDLE_FRICTION
            if left_vel[0] < 0:
                left_vel[0] = 0
        elif left_vel[0] < 0:
            left_vel[0] += PADDLE_FRICTION
            if left_vel[0] > 0:
                left_vel[0] = 0
    # Track acceleration for left paddle
    if left_moving:
        left_accel = min(PADDLE_ACCEL_MAX, left_accel + PADDLE_ACCEL_INC)
    else:
        left_accel = max(0.0, left_accel - PADDLE_ACCEL_DECAY)
    # Clamp speed
    left_vel[0] = max(-PADDLE_MAX_SPEED, min(PADDLE_MAX_SPEED, left_vel[0]))
    left_vel[1] = max(-PADDLE_MAX_SPEED, min(PADDLE_MAX_SPEED, left_vel[1]))
    # Update position
    left_paddle.x += int(left_vel[0])
    left_paddle.y += int(left_vel[1])
    # Keep in bounds
    left_paddle.x = max(0, min(left_paddle.x, WIDTH//2 - PADDLE_WIDTH))
    left_paddle.y = max(0, min(left_paddle.y, HEIGHT - PADDLE_HEIGHT))

    # AI for right paddle: track the ball with velocity and build acceleration (no randomness)
    right_moving = False
    if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
        right_vel[1] += PADDLE_ACC
        right_moving = True
    elif right_paddle.centery > ball.centery and right_paddle.top > 0:
        right_vel[1] -= PADDLE_ACC
        right_moving = True
    else:
        if right_vel[1] > 0:
            right_vel[1] -= PADDLE_FRICTION
            if right_vel[1] < 0:
                right_vel[1] = 0
        elif right_vel[1] < 0:
            right_vel[1] += PADDLE_FRICTION
            if right_vel[1] > 0:
                right_vel[1] = 0
    if right_paddle.centerx < ball.centerx and right_paddle.right < WIDTH:
        # Prevent right paddle from crossing the ball
        if right_paddle.left + right_vel[0] < ball.right and right_paddle.bottom > ball.top and right_paddle.top < ball.bottom:
            right_vel[0] += PADDLE_ACC
            right_moving = True
        else:
            right_paddle.x = ball.right
            right_vel[0] = 0
    elif right_paddle.centerx > ball.centerx and right_paddle.left > WIDTH//2:
        if right_paddle.right - right_vel[0] > ball.right and right_paddle.bottom > ball.top and right_paddle.top < ball.bottom:
            right_vel[0] -= PADDLE_ACC
            right_moving = True
        else:
            right_paddle.x = ball.right
            right_vel[0] = 0
    else:
        if right_vel[0] > 0:
            right_vel[0] -= PADDLE_FRICTION
            if right_vel[0] < 0:
                right_vel[0] = 0
        elif right_vel[0] < 0:
            right_vel[0] += PADDLE_FRICTION
            if right_vel[0] > 0:
                right_vel[0] = 0
    # Track acceleration for right paddle
    if right_moving:
        right_accel = min(PADDLE_ACCEL_MAX, right_accel + PADDLE_ACCEL_INC)
    else:
        right_accel = max(0.0, right_accel - PADDLE_ACCEL_DECAY)
    # Clamp speed
    right_vel[0] = max(-PADDLE_MAX_SPEED, min(PADDLE_MAX_SPEED, right_vel[0]))
    right_vel[1] = max(-PADDLE_MAX_SPEED, min(PADDLE_MAX_SPEED, right_vel[1]))
    # Update position
    right_paddle.x += int(right_vel[0])
    right_paddle.y += int(right_vel[1])
    # Keep in bounds
    right_paddle.x = max(WIDTH//2, min(right_paddle.x, WIDTH - PADDLE_WIDTH))
    right_paddle.y = max(0, min(right_paddle.y, HEIGHT - PADDLE_HEIGHT))


    # Ball movement with spin
    BALL_SPEED_Y -= BALL_SPIN * SPIN_EFFECT  # Reverse spin direction for expected behavior
    # Always build ball speed toward BALL_MAX_SPEED
    ball_speed = math.hypot(BALL_SPEED_X, BALL_SPEED_Y)
    if ball_speed < BALL_MAX_SPEED:
        # Accelerate ball toward max speed, preserving direction
        accel_factor = 1.004  # 0.4% increase per frame (30% slower)
        BALL_SPEED_X *= accel_factor
        BALL_SPEED_Y *= accel_factor
        # Clamp if we overshoot
        ball_speed = math.hypot(BALL_SPEED_X, BALL_SPEED_Y)
        if ball_speed > BALL_MAX_SPEED:
            scale = BALL_MAX_SPEED / ball_speed
            BALL_SPEED_X *= scale
            BALL_SPEED_Y *= scale
    elif ball_speed > BALL_MAX_SPEED:
        scale = BALL_MAX_SPEED / ball_speed
        BALL_SPEED_X *= scale
        BALL_SPEED_Y *= scale

    ball.x += int(BALL_SPEED_X)
    ball.y += int(BALL_SPEED_Y)
    BALL_SPIN *= SPIN_DECAY  # Spin decays over time


    # Ball collision with top/bottom: simple vertical bounce
    if ball.top < 0:
        ball.top = 0
        BALL_SPEED_Y *= -1
    if ball.bottom > HEIGHT:
        ball.bottom = HEIGHT
        BALL_SPEED_Y *= -1


    # Ball collision with paddles (with cooldown, angle, and spin)
    def ball_bounce(paddle, side, paddle_vel, paddle_accel):
        global BALL_SPEED_X, BALL_SPEED_Y, BALL_SPIN
        # Calculate hit position (relative to paddle center)
        rel = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
        max_angle = math.radians(60)
        angle = rel * max_angle
        # Use paddle_accel to boost outgoing speed
        base_speed = math.hypot(BALL_SPEED_X, BALL_SPEED_Y)
        speed_boost = 1.0 + (paddle_accel / PADDLE_ACCEL_MAX)  # 1.0 to 2.0 scale
        speed = base_speed * speed_boost
        # Clamp speed to max
        speed = min(speed, BALL_MAX_SPEED)
        min_momentum = 1.2 + paddle_accel * 0.15  # Lower minimum baseline (30% slower)
        # Divide paddle into three regions and apply separate bounce logic
        region_margin = paddle.width // 3
        if side == 'left':
            # Left paddle: left, center, right regions
            if ball.left <= paddle.left + region_margin:
                # Ball hit left edge region: do nothing (no bounce)
                return
            elif ball.right >= paddle.right - region_margin:
                # Ball hit right edge region: always bounce right
                BALL_SPEED_X = max(speed * math.cos(angle), min_momentum)
            else:
                # Center region: normal angle-based bounce
                BALL_SPEED_X = speed * math.cos(angle)
            BALL_SPEED_Y = speed * math.sin(angle)
            BALL_SPIN = paddle_vel[1] * 0.5
        else:
            # Right paddle: right, center, left regions
            if ball.right >= paddle.right - region_margin:
                # Ball hit right edge region: do nothing (no bounce)
                return
            elif ball.left <= paddle.left + region_margin:
                # Ball hit left edge region: always bounce left
                BALL_SPEED_X = -max(speed * math.cos(angle), min_momentum)
            else:
                # Center region: normal angle-based bounce (to the left)
                BALL_SPEED_X = -speed * math.cos(angle)
            BALL_SPEED_Y = speed * math.sin(angle)
            BALL_SPIN = paddle_vel[1] * 0.5

    # Only allow paddle to hit the ball if the ball is in front of the paddle
    if ball.colliderect(left_paddle):
        if last_hit != 'left' and ball.centerx > left_paddle.centerx:
            ball_bounce(left_paddle, 'left', left_vel, left_accel)
            last_hit = 'left'
            ai_react_delay = 80  # AI waits much longer before chasing ball again
    elif ball.colliderect(right_paddle):
        if last_hit != 'right' and ball.centerx < right_paddle.centerx:
            ball_bounce(right_paddle, 'right', right_vel, right_accel)
            last_hit = 'right'
    else:
        last_hit = None

    # Ball out of bounds and reset
    def reset_positions(direction):
        # Center paddles
        left_paddle.x = 10
        left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
        right_paddle.x = WIDTH - 20
        right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
        left_vel[0], left_vel[1] = 0, 0
        right_vel[0], right_vel[1] = 0, 0
        # Center ball
        ball.center = (WIDTH//2, HEIGHT//2)
        # Reset all ball physics
        global BALL_SPEED_X, BALL_SPEED_Y, BALL_SPIN
        BALL_SPIN = 0.0
        BALL_SPEED_Y = 0.0
        speed = 1.7  # Lower reset speed (30% slower)
        if direction == 'right':
            BALL_SPEED_X = speed
        else:
            BALL_SPEED_X = -speed

    # AI for right paddle: return to center after hit, react with delay
    if 'ai_react_delay' not in locals():
        ai_react_delay = 0
    ai_center_x = WIDTH*3//4
    ai_center_y = HEIGHT // 2
    if ai_react_delay > 0:
        ai_react_delay -= 1
        # Return to center of its box
        if abs(right_paddle.centerx - ai_center_x) > 5:
            if right_paddle.centerx < ai_center_x:
                right_vel[0] += PADDLE_ACC
            else:
                right_vel[0] -= PADDLE_ACC
        else:
            if right_vel[0] > 0:
                right_vel[0] -= PADDLE_FRICTION
                if right_vel[0] < 0:
                    right_vel[0] = 0
            elif right_vel[0] < 0:
                right_vel[0] += PADDLE_FRICTION
                if right_vel[0] > 0:
                    right_vel[0] = 0
        # Return to vertical center
        if abs(right_paddle.centery - ai_center_y) > 5:
            if right_paddle.centery < ai_center_y:
                right_vel[1] += PADDLE_ACC
            else:
                right_vel[1] -= PADDLE_ACC
        else:
            if right_vel[1] > 0:
                right_vel[1] -= PADDLE_FRICTION
                if right_vel[1] < 0:
                    right_vel[1] = 0
            elif right_vel[1] < 0:
                right_vel[1] += PADDLE_FRICTION
                if right_vel[1] > 0:
                    right_vel[1] = 0
    else:
        # Normal AI tracking
        if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
            right_vel[1] += PADDLE_ACC
        elif right_paddle.centery > ball.centery and right_paddle.top > 0:
            right_vel[1] -= PADDLE_ACC
        else:
            if right_vel[1] > 0:
                right_vel[1] -= PADDLE_FRICTION
                if right_vel[1] < 0:
                    right_vel[1] = 0
            elif right_vel[1] < 0:
                right_vel[1] += PADDLE_FRICTION
                if right_vel[1] > 0:
                    right_vel[1] = 0
        if right_paddle.centerx < ball.centerx and right_paddle.right < WIDTH:
            if right_paddle.left + right_vel[0] < ball.right:
                right_vel[0] += PADDLE_ACC
            else:
                right_paddle.x = ball.right
                right_vel[0] = 0
        elif right_paddle.centerx > ball.centerx and right_paddle.left > WIDTH//2:
            if right_paddle.right - right_vel[0] > ball.right:
                right_vel[0] -= PADDLE_ACC
            else:
                right_paddle.x = ball.right
                right_vel[0] = 0
        else:
            if right_vel[0] > 0:
                right_vel[0] -= PADDLE_FRICTION
                if right_vel[0] < 0:
                    right_vel[0] = 0
            elif right_vel[0] < 0:
                right_vel[0] += PADDLE_FRICTION
                if right_vel[0] > 0:
                    right_vel[0] = 0
    if ball.left <= 0:
        right_score += 1
        reset_positions('left')
    if ball.right >= WIDTH:
        left_score += 1
        reset_positions('right')

    # Drawing
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
