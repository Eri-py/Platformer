import sys, os
sys.dont_write_bytecode = True
from settings import *
from level import Level
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # Initialize screen
        self.clock = pygame.time.Clock()# Controls FPS

        self.tmx_map = {0: load_pygame(os.path.join(main_dir, "data","levels", "omni.tmx"))} # Contains all maps

        self.current_level = Level(self.tmx_map[0]) # Active level
        
    def event_handle(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Close game when X is pressed
                pygame.quit
                sys.exit()
            self.current_level.player.input(event)

    def run(self) -> None:
        while True:
            dt = self.clock.tick()/1000
            self.event_handle()
            self.current_level.run(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()