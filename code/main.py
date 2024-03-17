import sys
sys.dont_write_bytecode = True
from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()

        self.tmx_maps = {0: load_pygame(join(main_dir, "data", "levels", "Omni.tmx"))} # all maps

        self.current_level = Level(self.tmx_maps[0])
    
    def event_handle(self) -> None: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def run(self) -> None:
        while True:
            dt = self.clock.tick()/1000
            self.event_handle()
            self.current_level.run(dt) 
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
