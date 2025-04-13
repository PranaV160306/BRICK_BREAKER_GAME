import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

# Game variables
score = 0
lives = 3
game_over = False
game_won = False

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 8

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = -4

# Bricks
brick_colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN]
bricks = []

def create_bricks():
    bricks.clear()
    for row in range(5):
        for col in range(WIDTH // BRICK_WIDTH):
            brick = pygame.Rect(col * BRICK_WIDTH + 5, row * BRICK_HEIGHT + 50, BRICK_WIDTH - 10, BRICK_HEIGHT - 5)
            bricks.append((brick, brick_colors[row % len(brick_colors)]))

create_bricks()

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    global ball_speed_x, ball_speed_y
    ball_speed_x = 4 * random.choice((1, -1))
    ball_speed_y = -4

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def show_menu():
    screen.fill(BLACK)
    draw_text("BRICK BREAKER", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    draw_text("Press SPACE to Start", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Use LEFT and RIGHT arrows to move", 24, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_loop():
    global score, lives, game_over, game_won, ball_speed_x, ball_speed_y
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if (game_over or game_won) and event.key == pygame.K_SPACE:
                    # Reset game
                    score = 0
                    lives = 3
                    game_over = False
                    game_won = False
                    create_bricks()
                    reset_ball()
                    paddle.centerx = WIDTH // 2
        
        if not game_over and not game_won:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.x -= paddle_speed
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.x += paddle_speed
            
            # Ball movement
            ball.x += ball_speed_x
            ball.y += ball_speed_y
            
            # Ball collision with walls
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1
            
            # Ball collision with paddle
            if ball.colliderect(paddle) and ball_speed_y > 0:
                ball_speed_y *= -1
                # Add some angle variation based on where ball hits paddle
                offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH / 2)
                ball_speed_x = offset * 5
            
            # Ball goes out of bottom
            if ball.top > HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    reset_ball()
            
            # Ball collision with bricks
            for brick, color in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove((brick, color))
                    ball_speed_y *= -1
                    score += 10
                    break
            
            # Check if all bricks are destroyed
            if not bricks:
                game_won = True
        
        # Drawing
        screen.fill(BLACK)
        
        if game_over:
            draw_text("GAME OVER", 64, RED, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Final Score: {score}", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text("Press SPACE to Play Again", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        elif game_won:
            draw_text("YOU WIN!", 64, GREEN, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Final Score: {score}", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text("Press SPACE to Play Again", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        else:
            # Draw paddle
            pygame.draw.rect(screen, WHITE, paddle)
            
            # Draw ball
            pygame.draw.ellipse(screen, WHITE, ball)
            
            # Draw bricks
            for brick, color in bricks:
                pygame.draw.rect(screen, color, brick)
            
            # Draw score and lives
            draw_text(f"Score: {score}", 36, WHITE, 70, 20)
            draw_text(f"Lives: {lives}", 36, WHITE, WIDTH - 70, 20)
        
        pygame.display.flip()
        clock.tick(FPS)

# Start the game
show_menu()
game_loop()