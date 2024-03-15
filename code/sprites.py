from settings import *
from random import choice

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(choice(["blue", "white", "yellow", "purple", "green", "pink"]))
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()