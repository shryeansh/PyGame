# file: level3_collisions.py
import pygame, sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 3: Collisions")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# --- player (a rectangle) ---
PLAYER_SIZE = 50
player = pygame.Rect(WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 30, PLAYER_SIZE, PLAYER_SIZE)
PLAYER_SPEED = 6

# --- obstacles (rectangles) ---
# static block
block = pygame.Rect(480, 220, 140, 70)
# moving block (slides left-right)
mover = pygame.Rect(120, 140, 120, 50)
mover_speed = 4

def draw_text(text, x, y, color=(230,230,230)):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

running = True
while running:
    dt = clock.tick(60)  # limit to 60 FPS
    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # --- input & movement ---
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])
    player.x += dx * PLAYER_SPEED
    player.y += dy * PLAYER_SPEED

    # keep player within window
    player.clamp_ip(screen.get_rect())

    # --- move the moving obstacle ---
    mover.x += mover_speed
    if mover.right >= WIDTH or mover.left <= 0:
        mover_speed *= -1  # bounce

    # --- collision checks ---
    hit_static = player.colliderect(block)
    hit_mover  = player.colliderect(mover)
    collided   = hit_static or hit_mover

    # --- draw ---
    screen.fill((24, 24, 32))

    # draw obstacles
    pygame.draw.rect(screen, (200, 140, 60), block)         # static
    pygame.draw.rect(screen, (120, 160, 255), mover)        # moving

    # draw player (turn red if colliding)
    color = (80, 220, 120) if not collided else (220, 80, 80)
    pygame.draw.rect(screen, color, player)

    # outlines (to visualize hitboxes)
    pygame.draw.rect(screen, (50,50,50), block, 2)
    pygame.draw.rect(screen, (50,50,50), mover, 2)
    pygame.draw.rect(screen, (230,230,230), player, 2)

    # UI text
    draw_text("WASD / Arrows to move", 10, 10)
    draw_text("Collision: " + ("YES" if collided else "no"), 10, 44, (255,100,100) if collided else (130,220,130))

    pygame.display.flip()
