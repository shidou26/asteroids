import pygame 
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # screen init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # clock init
    clock = pygame.time.Clock()
    dt = 0.0

    # group init
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # player init
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 

        # rendering
        updatable.update(dt)
        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen) 

        # update screen
        pygame.display.flip()

        # update clock
        dt = clock.tick(60) / 1000
        print(f"Delta time: {dt}")

if __name__ == "__main__":
    main()
