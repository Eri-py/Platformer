from settings import *
from sprites import Sprite, MovingSprite
from player import Player

class Level:
    def __init__(self, tmx_map) -> None:
        self.display = pygame.display.get_surface()

        #sprite groups
        self.visible_sprite_group = pygame.sprite.Group()
        self.collision_sprite_group =pygame.sprite.Group()
        
        self.setup(tmx_map)

    def setup(self, tmx_map) -> None:
        #tiles
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), surf, [self.visible_sprite_group, self.collision_sprite_group])
        
        #objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                Player((obj.x, obj.y), self.visible_sprite_group, self.collision_sprite_group)
        
        #moving objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "platform":
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties["speed"]
                MovingSprite(start_pos, end_pos, move_dir, speed, [self.visible_sprite_group, self.collision_sprite_group])
     
    def run(self, dt) -> None:
        self.display.fill("black")
        #draw images
        self.visible_sprite_group.update(dt)
        self.visible_sprite_group.draw(self.display)

