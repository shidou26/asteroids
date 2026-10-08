import pygame 
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius) 

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        if new_radius == 0:
            return None
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        left_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        left_asteroid.velocity = self.velocity.rotate(angle) * 1.2
        right_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        right_asteroid.velocity = self.velocity.rotate(-angle) * 1.2
        
        