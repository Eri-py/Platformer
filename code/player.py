from settings import *
from timer import Timer
from pygame.image import load
from os.path import join
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.display = pygame.display.get_surface()
        # image
        self.image = load(join(main_dir, "graphics", "player", "idle", "0.png"))
        # rects
        self.rect = self.image.get_frect(topleft=pos).inflate(0, 5)
        self.hitbox_rect = self.rect.inflate(-14, -9)
        self.old_rect = self.hitbox_rect.copy()
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
        self.timers = {"wall jump": Timer(250), "wall jump block": Timer(1000)}

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
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        # vertical
        if not self.on_surface["floor"] and any((self.on_surface["left"], self.on_surface["right"])): # wall slide
            if not self.timers["wall jump block"].active: 
                self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else: # regular fall
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        
        self.rect.center = self.hitbox_rect.center
        
        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height  # Regular jump
                self.hitbox_rect.y -= 1
            elif any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall jump block"].active:
                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height # Wall Jump
                self.direction.x = 0.5 if self.on_surface["left"] else -0.5
                self.timers["wall jump block"].activate()
            self.jump = False
        
        self.collision("vertical")
            
    def platform_move(self, dt) -> None: #player movement on platform
        if self.platform:
            self.hitbox_rect.center += self.platform.direction * self.platform.speed * dt
    
    def check_contact(self) -> None: # checks current collision surface
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2)))
        left_rect  = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2)))
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
            if self.hitbox_rect.colliderect(sprite.rect):
                if axis == "horizontal":
                    # left
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    # right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else: # vertical
                    # top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, "moving"):
                            self.hitbox_rect.top += 6
                    # bottom
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
    
    def update_timer(self) -> None: # runs update method for all timers in self.timers
        for timer in self.timers.values():
            timer.update()

    def update(self, dt) -> None: # updates sprites
        self.old_rect = self.hitbox_rect.copy()
        self.input()
        self.update_timer()
        self.move(dt) 
        self.platform_move(dt)
        self.check_contact()



