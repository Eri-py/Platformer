from settings import *
from sprites import Sprite, MovingSprites
from player import Player

class Level:
    def __init__(self, tmx_map) -> None:
        self.display_surf = pygame.display.get_surface()
        # Groups
        self.visible_sprites_group = pygame.sprite.Group()
        self.collision_sprite_group = pygame.sprite.Group()

        self.setup(tmx_map)
    
    def setup(self, tmx_map) -> None:
        # Tiles
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), surf, [self.visible_sprites_group, self.collision_sprite_group])

        # Player
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                self.player = Player((obj.x, obj.y), self.visible_sprites_group, self.collision_sprite_group)
        
        # Moving objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "platform":
                if obj.width > obj.height: # Horizontal
                    move_dir = "x"
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else:
                    move_dir = "y"
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties["speed"]
                MovingSprites(start_pos, end_pos, move_dir, speed, [self.visible_sprites_group, self.collision_sprite_group])

    def run(self, dt) -> None:
        self.display_surf.fill("black")
        self.visible_sprites_group.draw(self.display_surf)
        self.visible_sprites_group.update(dt)