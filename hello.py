# file: level4_enemies_scoring.py
import pygame, sys, random
pygame.init()

# --- setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 4: Scoring & Enemies")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- player ---
PLAYER_SIZE = 50
PLAYER_SPEED = 320  # pixels/second (time-based movement)
player = pygame.Rect(WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 24, PLAYER_SIZE, PLAYER_SIZE)

# --- enemies ---
enemies = []
SPAWN_INTERVAL = 0.7   # seconds between spawns (base)
spawn_timer = 0.0

def spawn_enemy():
    w = random.randint(30, 70)
    x = random.randint(0, WIDTH - w)
    y = -w
    vy = random.randint(160, 340)  # fall speed px/s
    color = (random.randint(120,255), random.randint(90,200), random.randint(90,200))
    return {"rect": pygame.Rect(x, y, w, w), "vy": vy, "color": color}

# --- game state ---
alive = True
score = 0.0

def reset():
    global player, enemies, spawn_timer, alive, score
    player.update(WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 24, PLAYER_SIZE, PLAYER_SIZE)
    enemies.clear()
    spawn_timer = 0.0
    alive = True
    score = 0.0

# --- loop ---
while True:
    dt = clock.tick(60) / 1000.0  # seconds since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.key == pygame.K_r and not alive:
                reset()

    # input & movement (time-based)
    keys = pygame.key.get_pressed()
    if alive:
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])
        player.x += int(dx * PLAYER_SPEED * dt)
        player.y += int(dy * PLAYER_SPEED * dt)
        player.clamp_ip(screen.get_rect())

        # spawn enemies over time (light difficulty curve)
        spawn_timer += dt
        interval = max(0.30, SPAWN_INTERVAL - score * 0.02)  # gets a bit harder as score grows
        while spawn_timer >= interval:
            enemies.append(spawn_enemy())
            spawn_timer -= interval

        # move enemies & cull off-screen
        for e in enemies:
            e["rect"].y += int(e["vy"] * dt)
        enemies = [e for e in enemies if e["rect"].top <= HEIGHT]

        # collision
        for e in enemies:
            if player.colliderect(e["rect"]):
                alive = False
                break

        # scoring
        score += dt

    # --- draw ---
    screen.fill((22, 22, 30))
    # enemies
    for e in enemies:
        pygame.draw.rect(screen, e["color"], e["rect"])
    # player
    pygame.draw.rect(screen, (80, 220, 120) if alive else (140, 140, 140), player)
    # UI
    screen.blit(font.render(f"Score: {score:.1f}", True, (235,235,235)), (10, 10))
    screen.blit(font.render("Arrows/WASD to move", True, (180,180,200)), (10, 44))
    if not alive:
        msg = font.render("Game Over — R to Restart, Esc to Quit", True, (255,120,120))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))

    pygame.display.flip()
