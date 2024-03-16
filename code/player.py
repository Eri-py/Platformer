from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites) -> None:
        super().__init__(groups)
        # Sprite
        self.image = pygame.Surface((16, 27))
        self.image.fill("red")
        # Rects
        self.rect = self.image.get_frect(center=pos)
        self.old_rect = self.rect.copy()
        # Movement
        self.direction = vector()
        self.speed = 400
        # Fall
        self.gravity = 1300
        # Jump
        self.jump_height = 595
        self.jump_index = 0
        # Collisions
        self.collision_sprites = collision_sprites

    def input(self, event) -> None:
        keys = pygame.key.get_pressed()
        # Right motion
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        # Left motion
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        # Stop motion
        else:
            self.direction.x = 0
        # Jump
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 5))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if(floor_rect.collidelist([sprite.rect for sprite in self.collision_sprites.sprites()]) >= 0) and self.jump_index == 0:
                self.direction.y = -self.jump_height
            if self.jump_index == 1:
                self.direction.y = -self.jump_height
            self.jump_index += 1

    def move(self, dt) -> None:
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed * dt
        self.check_collisions("horizontal", dt)
        # Vertical movement
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.check_collisions("vertical", dt)

    def check_collisions(self, axis, dt) -> None:
        # Moving platform collisions
        for sprite in self.collision_sprites:
            if hasattr(sprite, "moving"):
                if self.rect.bottom == sprite.rect.top:
                    self.rect.center += sprite.direction * sprite.speed * dt
        # Regular ground collisions
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == "vertical":
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.jump_index = 0
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                elif axis == "horizontal":
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.jump_index = 1
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.move(dt)

