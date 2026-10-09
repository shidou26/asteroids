import pygame 
pygame.mixer.init()

freedom_sound = pygame.mixer.Sound("./art/shoot.wav")
crash_sound = pygame.mixer.Sound("./art/crash.mp3")

def play_freedom() -> None:
    freedom_sound.play() 

def play_crash() -> None:
    crash_sound.play()

    