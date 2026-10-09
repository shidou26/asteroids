import pygame 
import music
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from constants import ASTEROID_KINDS, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # screen init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("./art/background.jpg")
    pygame.display.set_caption("Asteroids")

    # clock init
    clock = pygame.time.Clock()
    dt = 0.0

    # music init
    pygame.mixer.music.load("./art/start.wav")
    pygame.mixer.music.play(-1)

    # group init
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # player init
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # asteroids init
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    field = AsteroidField()

    # freedom init
    Shot.containers = (updatable, drawable, shots)

    # score
    total_point = 0
    font = pygame.font.Font("./art/press_start.ttf", 26)
    big_font = pygame.font.Font("./art/press_start.ttf", 30)

    # game state
    in_menu = True 
    in_game_over = False
    welcome_text = big_font.render("Asteroids in the big 2026", True, "white")
    start_text = font.render("START", True, "white")
    start_rect = start_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    quit_text = font.render("QUIT", True, "white")
    quit_rect = quit_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

    # game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if in_menu:
                    if start_rect.collidepoint(event.pos):
                        in_menu = False 
                        pygame.mixer.stop()
                        pygame.mixer.music.load("./art/music.mp3")
                        pygame.mixer.music.play(-1)
                    elif quit_rect.collidepoint(event.pos):
                        return
                if in_game_over:
                    if quit_rect.collidepoint(event.pos):
                        return
        
        screen.blit(background, (0, 0))

        if in_menu:
            screen.blit(welcome_text, welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)))
            screen.blit(start_text, start_rect)
            screen.blit(quit_text, quit_rect)

        if in_game_over:
            final_score = font.render(f"Score:{total_point}", True, "white")
            screen.blit(final_score, final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if not in_menu and not in_game_over:
            # updating
            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    in_game_over = True
                    pygame.mixer.stop()
                    pygame.mixer.music.load("./art/game_over.mp3")
                    pygame.mixer.music.play(-1)
                    break
                for shot in shots:
                    if asteroid.collides_with(shot):
                        total_point += (ASTEROID_KINDS - asteroid.radius // ASTEROID_MIN_RADIUS + 1) * 10
                        log_event("asteroid_shot")
                        music.play_crash()
                        shot.kill()
                        asteroid.split()
                        break 
            # drawing
            for drawing in drawable:
                drawing.draw(screen) 
            text = font.render(f"Score:{total_point}", True, "white")
            screen.blit(text, (16, 10))

        # update screen
        pygame.display.flip()
        # update clock
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
