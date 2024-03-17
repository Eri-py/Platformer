from settings import *
from timer import Timer
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites) -> None:
        super().__init__(groups)
        # image
        self.image = pygame.Surface((16, 27))
        self.image.fill("red")
        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        # movement
        self.direction = vector()
        self.speed = 300
        self.gravity = 1300
        self.jump = False
        self.jump_height = 595 
        #collisions
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}     
        self.platform = None
        #timer
        self.timers = {"wall jump": Timer(250), "wall jump block": Timer(500)}

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if not self.timers["wall jump"].active: # disable movement on a wall
            # right
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1
                # left
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1
            self.direction.x = input_vector.normalize().x if input_vector else 0
        # jump
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def move(self, dt) -> None: # controls all player motion
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        # platform
        if self.platform:
            if abs(self.platform.direction.x) == 1:
                self.rect.topleft += self.platform.direction * self.platform.speed * dt

        self.collision("horizontal")

        # vertical
        if not self.on_surface["floor"] and any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall jump block"].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        # platform
        if self.platform:
            if abs(self.platform.direction.y) == 1:
                self.rect.topleft += self.platform.direction * self.platform.speed * dt * 0.75
        
        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height  # Regular jump
                self.rect.y -= 1
            elif any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall jump block"].active:
                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 0.5 if self.on_surface["left"] else -0.5
                self.timers["wall jump block"].activate()
            self.jump = False
        
        self.collision("vertical")
    
    def check_contact(self) -> None: # checks current collision surface
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect((self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2)))
        left_rect  = pygame.Rect((self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2)))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # collisions
        self.on_surface["floor"] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface["left"]  = True if left_rect.collidelist(collide_rects)  >= 0 else False
        self.on_surface["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False
        
        # platforms
        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, "moving")]:
            if floor_rect.colliderect(sprite.rect):
                self.platform = sprite
    
    def collision(self, axis) -> None: 
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == "horizontal":
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else: # vertical
                    # top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
    
    def update_timer(self) -> None: # runs update method for all timers in self.timers
        for timer in self.timers.values():
            timer.update()

    def update(self, dt) -> None: # updates sprites
        self.old_rect = self.rect.copy()
        self.input()
        self.update_timer()
        self.move(dt) 
        self.check_contact()



