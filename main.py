import pygame 
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

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
    asteroids = pygame.sprite.Group()

    # player init
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # asteroids init
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    field = AsteroidField()

    # game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 

        # updating
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # drawing
        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen) 
        

        # update screen
        pygame.display.flip()

        # update clock
        dt = clock.tick(60) / 1000
        # print(f"Delta time: {dt}")

if __name__ == "__main__":
    main()
