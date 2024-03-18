from settings import *

class Allsprites(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_pos) -> None:
        self.offset.x = -(target_pos[0] - SCREENWIDTH / 2)
        self.offset.y = -(target_pos[1] - SCREENHEIGHT / 2)
        for sprite in self:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)