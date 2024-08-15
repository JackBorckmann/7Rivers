import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rabbit Jump")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (34, 139, 34)   # Forest green

# Load images
rabbit_img = pygame.Surface((40, 60))  # Placeholder for rabbit image
rabbit_img.fill((255, 192, 203))  # Light pink color for visibility
cloud_img = pygame.Surface((80, 40))  # Placeholder for cloud image
cloud_img.fill(WHITE)

# Player properties
player_width = 40
player_height = 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 150
player_speed = 5
jump_speed = -10
gravity = 0.4

# Platform properties
platform_width = 80
platform_height = 20
platform_count = 10
platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 50]]

# Cloud properties
clouds = []
for _ in range(5):
    clouds.append([random.randint(0, WIDTH - 80), random.randint(0, HEIGHT)])

# Game variables
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

def reset_game():
    global player_x, player_y, jump_speed, score, platforms
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 150
    jump_speed = -10
    score = 0
    platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 50]]
    for i in range(1, platform_count):
        x = random.randint(0, WIDTH - platform_width)
        y = HEIGHT - (i * HEIGHT // platform_count)
        platforms.append([x, y])

def draw_clouds():
    for cloud in clouds:
        screen.blit(cloud_img, cloud)
        cloud[1] += 1
        if cloud[1] > HEIGHT:
            cloud[1] = -40
            cloud[0] = random.randint(0, WIDTH - 80)

def game_loop():
    global player_x, player_y, jump_speed, score, high_score

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Apply gravity
        jump_speed += gravity
        player_y += jump_speed

        # Check for collision with platforms
        for platform in platforms:
            if (player_y + player_height >= platform[1] and
                player_y + player_height <= platform[1] + platform_height and
                player_x + player_width > platform[0] and
                player_x < platform[0] + platform_width):
                jump_speed = -10

        # Move screen down and add new platforms
        if player_y < HEIGHT // 2:
            player_y += abs(jump_speed)
            for platform in platforms:
                platform[1] += abs(jump_speed)
                if platform[1] > HEIGHT:
                    platforms.remove(platform)
                    score += 1
                    x = random.randint(0, WIDTH - platform_width)
                    y = random.randint(-50, -10)
                    platforms.append([x, y])

        # Wrap player around screen edges
        if player_x < -player_width:
            player_x = WIDTH
        elif player_x > WIDTH:
            player_x = -player_width

        # Game over condition
        if player_y > HEIGHT:
            high_score = max(score, high_score)
            return "GAME_OVER"

        # Clear the screen
        screen.fill(BLUE)

        # Draw clouds
        draw_clouds()

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, (platform[0], platform[1], platform_width, platform_height))

        # Draw player (rabbit)
        screen.blit(rabbit_img, (player_x, player_y))

        # Draw scores
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

def game_over_screen():
    screen.fill(BLUE)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    play_again_text = font.render("Press SPACE to play again or Q to quit", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "PLAY_AGAIN"
                elif event.key == pygame.K_q:
                    return "QUIT"

# Main game loop
while True:
    reset_game()
    result = game_loop()
    if result == "QUIT":
        break
    elif result == "GAME_OVER":
        choice = game_over_screen()
        if choice == "QUIT":
            break
        # If choice is "PLAY_AGAIN", the loop continues and resets the game

pygame.quit()
sys.exit()