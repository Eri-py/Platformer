from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map) -> None:
        self.display_surf = pygame.display.get_surface()
        #groups
        self.visible_sprites_group = pygame.sprite.Group()
        self.collision_sprite_group = pygame.sprite.Group()

        self.setup(tmx_map)
    
    def setup(self, tmx_map) -> None:
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), surf, [self.visible_sprites_group, self.collision_sprite_group])
    
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                self.player = Player((obj.x, obj.y), self.visible_sprites_group, self.collision_sprite_group)

    def run(self, dt) -> None:
        self.display_surf.fill("black")
        self.visible_sprites_group.draw(self.display_surf)
        self.visible_sprites_group.update(dt)