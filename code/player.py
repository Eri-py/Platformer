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
        self.movement_vector = vector()
        self.speed = 400
        #fall
        self.gravity = 1300
        self.jump_height = 715
        self.jump_index = 0
        #collisions
        self.collision_sprites = collision_sprites

    def input(self, event) -> None:
        #Keyboard movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT: #right movement
                self.movement_vector.x = 1 
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.movement_vector.x = -1 #left movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                self.movement_vector.x = 0  #stop movement
        #jump motion - keyboard
        pass
        #Controller movement
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 14: 
                self.movement_vector.x = 1 #right movement
            elif event.button == 13:
                self.movement_vector.x = -1 #left movement
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 14 or event.button == 13:
                self.movement_vector.x = 0 #stop movement
        
    def move(self, dt) -> None:
        #horizontal
        self.rect.x += self.movement_vector.x * self.speed * dt
        self.collision("horizontal")
        #vertical movement / gravity
        self.movement_vector.y += self.gravity / 2 * dt
        self.rect.y += self.movement_vector.y * dt
        self.movement_vector.y += self.gravity / 2 * dt
        self.collision("vertical")
        
    def collision(self, axis) -> None:
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if axis == "vertical":
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.movement_vector.y = 0
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