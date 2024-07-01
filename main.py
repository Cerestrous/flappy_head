import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GROUND_HEIGHT = 50
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds

# Set up the display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Ninja')

# Load the player image with transparent background
player_image_path = 'ninja_sprite.png'  # Using the provided image
player_image = pygame.image.load(player_image_path).convert_alpha()
player_rect = player_image.get_rect()
player_rect.topleft = (100, WINDOW_HEIGHT // 2)

# Load the background and ground images
background_color = (135, 206, 250)  # Sky blue
ground_color = (145, 100, 0)  # Brown

# Pipe image
pipe_image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT)).convert_alpha()
pipe_image.fill((0, 255, 0))  # Green

# Player physics
player_velocity = 0

# Event for creating pipes
pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

# Function to create new pipes
def create_pipe():
    height = random.randint(150, 400)
    top_pipe = pipe_image.get_rect(midbottom=(WINDOW_WIDTH + PIPE_WIDTH, height - PIPE_GAP // 2))
    bottom_pipe = pipe_image.get_rect(midtop=(WINDOW_WIDTH + PIPE_WIDTH, height + PIPE_GAP // 2))
    return top_pipe, bottom_pipe

# List to store pipes
pipes = []

# Game state
game_active = True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player_velocity = JUMP_STRENGTH
            if event.key == pygame.K_r and not game_active:
                # Reset game
                player_rect.topleft = (100, WINDOW_HEIGHT // 2)
                player_velocity = 0
                pipes = []
                game_active = True
        if event.type == pygame.USEREVENT and game_active:
            pipes.extend(create_pipe())

    if game_active:
        # Apply gravity
        player_velocity += GRAVITY
        player_rect.y += player_velocity

        # Check for collisions with ground
        if player_rect.bottom >= WINDOW_HEIGHT - GROUND_HEIGHT:
            player_rect.bottom = WINDOW_HEIGHT - GROUND_HEIGHT
            game_active = False

        # Move pipes
        for pipe in pipes:
            pipe.centerx -= PLAYER_SPEED

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.right > 0]

        # Check for collisions with pipes
        for pipe in pipes:
            if player_rect.colliderect(pipe):
                game_active = False

    # Clear the screen
    window.fill(background_color)

    # Draw the ground
    pygame.draw.rect(window, ground_color, (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))

    # Draw the player
    window.blit(player_image, player_rect.topleft)

    # Draw the pipes
    for pipe in pipes:
        window.blit(pipe_image, pipe.topleft)

    if not game_active:
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('YOU LOSE!', True, (255, 0, 0))
        window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = font.render('Press R to Restart', True, (255, 255, 255))
        window.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + game_over_text.get_height()))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()