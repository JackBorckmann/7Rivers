import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rabbit Jump")

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Player properties
player_width = 30
player_height = 50
player_speed = 5
player_jump = -13  # Increased jump height
gravity = 0.5

# Platform properties
platform_width = 100
platform_height = 20

# Font
font = pygame.font.Font(None, 36)

# Cloud properties
clouds = []

def create_cloud():
    x = random.randint(-50, WIDTH)
    y = random.randint(0, HEIGHT // 2)
    speed = random.uniform(0.1, 0.5)
    return [x, y, speed]

def draw_cloud(cloud):
    x, y, _ = cloud
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 20)
    pygame.draw.circle(screen, WHITE, (int(x + 15), int(y - 10)), 15)
    pygame.draw.circle(screen, WHITE, (int(x + 30), int(y)), 20)

def reset_game():
    global player_x, player_y, player_velocity, platforms, score, clouds
    
    # Reset player position
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 70
    player_velocity = 0
    
    # Reset platforms
    platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 50, platform_width, platform_height]]
    for i in range(10):
        create_platform()
    
    # Reset score
    score = 0
    
    # Create clouds
    clouds = [create_cloud() for _ in range(5)]

def create_platform():
    x = random.randint(0, WIDTH - platform_width)
    y = platforms[-1][1] - random.randint(80, 120)  # Increased gap
    platforms.append([x, y, platform_width, platform_height])

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_rabbit(x, y):
    # Body
    pygame.draw.ellipse(screen, BROWN, (x, y + 10, player_width, player_height - 20))
    # Head
    pygame.draw.circle(screen, BROWN, (x + player_width // 2, y), 15)
    # Ears
    pygame.draw.ellipse(screen, BROWN, (x + 5, y - 20, 10, 25))
    pygame.draw.ellipse(screen, BROWN, (x + player_width - 15, y - 20, 10, 25))
    # Eyes
    pygame.draw.circle(screen, RED, (x + player_width // 2 - 5, y - 2), 2)
    pygame.draw.circle(screen, RED, (x + player_width // 2 + 5, y - 2), 2)

# Initialize game variables
score = 0
high_score = 0
reset_game()

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()
                game_over = False
            elif event.key == pygame.K_q:
                running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Apply gravity
        player_velocity += gravity
        player_y += player_velocity

        # Check collision with platforms
        for platform in platforms:
            if (player_y + player_height >= platform[1] and 
                player_y + player_height <= platform[1] + platform[3] and
                player_x + player_width > platform[0] and 
                player_x < platform[0] + platform[2] and 
                player_velocity > 0):
                player_velocity = player_jump

        # Move screen up if player is in upper half
        if player_y < HEIGHT // 2:
            player_y += abs(player_jump)
            for platform in platforms:
                platform[1] += abs(player_jump)
            score += 1

            # Remove platforms that are off screen and create new ones
            while platforms[-1][1] >= 0:
                create_platform()
            platforms = [p for p in platforms if p[1] < HEIGHT]

        # Check if player has fallen off the screen
        if player_y > HEIGHT:
            game_over = True
            if score > high_score:
                high_score = score

        # Move and wrap clouds
        for cloud in clouds:
            cloud[0] += cloud[2]
            if cloud[0] > WIDTH + 50:
                cloud[0] = -50
                cloud[1] = random.randint(0, HEIGHT // 2)

    # Clear the screen
    screen.fill(SKY_BLUE)

    # Draw clouds
    for cloud in clouds:
        draw_cloud(cloud)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Draw player (rabbit)
    draw_rabbit(player_x, player_y)

    # Draw score
    draw_text(f"Score: {score}", BLACK, WIDTH // 2, 30)
    draw_text(f"High Score: {high_score}", BLACK, WIDTH // 2, 60)

    if game_over:
        draw_text("Game Over!", RED, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press SPACE to play again", BLACK, WIDTH // 2, HEIGHT // 2)
        draw_text("Press Q to quit", BLACK, WIDTH // 2, HEIGHT // 2 + 50)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()