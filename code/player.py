from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites) -> None:
        super().__init__(groups)
        #sprite
        self.image = pygame.Surface((16,27))
        self.image.fill("red")
        #controller
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())] #number of active controllers
        #rects
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()     
        #movement
        self.direction = vector()
        self.speed = 400
        #fall
        self.gravity = 1300
        #jump
        self.jump_height = 595
        self.jump_count = 0
        self.max_jumps = 2
        #collisions
        self.collision_sprites = collision_sprites

    def input(self, event) -> None:
        #Keyboard movement
        keys = pygame.key.get_pressed() # return dictionary containing all keys and a boolean 
        #right motion
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        #left motion
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        #stop motion
        else:
            self.direction.x = 0 
        #jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.jump()   
             
    def move(self, dt) -> None:
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        #vertical movement / gravity
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision("vertical")
    
    def jump(self):
        if (self.rect.bottom <= sprite.rect.top for sprite in self.collision_sprites) and self.jump_count < self.max_jumps:
            self.direction.y = -self.jump_height
            self.jump_count +=1 
            
    def collision(self, axis) -> None:
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == "vertical":
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.jump_count = 0
                    #top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                if axis == "horizontal":
                    #right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    #left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                                    
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.move(dt)