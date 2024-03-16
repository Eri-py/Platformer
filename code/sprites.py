from settings import *
from random import choice

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILESIZE, TILESIZE)), groups = None) -> None:
        super().__init__(groups)
        self.image = surf
        self.image.fill("white")
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

class MovingSprites(Sprite):
    def __init__(self, start_pos, end_pos, move_dir, speed, groups) -> None:
        surf = pygame.Surface((150, 20))
        super().__init__(start_pos, surf, groups)
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        #movement
        self.speed = speed
        self.move_dir = move_dir
        self.direction = vector(1,0) if move_dir == "x" else vector(0,1)
        self.moving = True

    def check_border(self) -> None:
        if self.move_dir == "x":
            if self.rect.right >= self.end_pos[0]:
                self.direction.x = -1
            if self.rect.left <= self.start_pos[0]:
                self.direction.x = 1
        if self.move_dir == "y":
            if self.rect.bottom >= self.end_pos[1]:
                self.direction.y = -1
            if self.rect.top <= self.start_pos[1]:
                self.direction.y = 1
        
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.rect.center += self.direction * self.speed * dt
        self.check_border()