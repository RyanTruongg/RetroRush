import pygame
import utils


class Effect(pygame.sprite.Sprite):

    def __init__(self, frames: list[pygame.Surface], **kwargs) -> None:
        super().__init__()
        self.animation_idx = 0
        self.frames = frames
        if len(self.frames) > 0:
            self.image = self.frames[self.animation_idx]
            self.rect = self.image.get_rect(**kwargs)

    def update(self):
        self.animation_idx += 0.3
        if self.animation_idx > len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.animation_idx)]


class Player(pygame.sprite.Sprite):
    jump_frames = utils.split_from('graphics\\character\\jump_48.png', 48, 2)
    A_RUN = 'run'
    A_SWORD_RUN = 'sword_run'
    A_JUMP = 'jump'
    A_JUMP_MAX = 'jump_max'
    A_IDLE = 'idle'
    A_SWORD_IDLE = 'sword_idle'
    A_FALL = 'fall'
    A_SWORD_ATTACK = 'sword_attack'
    ANIMATIONS = {
        A_IDLE:
        utils.split_from('graphics\\character\\idle_48.png', 48, 2),
        A_SWORD_IDLE:
        utils.split_from('graphics\\character\\sword\\sword_idle_48.png', 48,
                         2),
        A_RUN:
        utils.split_from('graphics\\character\\run_48.png', 48, 2),
        A_SWORD_RUN:
        utils.split_from('graphics\\character\\sword\\sword_run_48.png', 48,
                         2),
        A_JUMP: [jump_frames[0]],
        A_JUMP_MAX: [jump_frames[1]],
        A_FALL: [jump_frames[2]],
        A_SWORD_ATTACK:
        utils.split_from('graphics\\character\\sword\\sword_attack_64.png', 64,
                         2),
    }

    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.effects_group = pygame.sprite.Group()

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.base_gravity = 0.6
        self.gravity = self.base_gravity
        self.on_ground = False

        self.animation_idx = 0
        self.animation_speed = 0.2
        self.flip_image = False
        self.has_sword = True
        self.sword_attacking = False

        self.image = Player.ANIMATIONS[self.get_animation_status()][0]
        self.hit_box_rect = self.image.get_rect(bottomleft=position)
        self.hit_box_rect.size = (32, 64)
        self.rect = self.hit_box_rect.copy()

    def get_animation_status(self):
        if self.sword_attacking:
            self.animation_speed = 0.4
            return Player.A_SWORD_ATTACK
        if self.direction.y < 0:
            return Player.A_JUMP
        if self.direction.y > 0:
            return Player.A_FALL
        if self.direction.x != 0:
            self.animation_speed = 0.2
            if self.has_sword:
                return Player.A_SWORD_RUN
            else:
                return Player.A_RUN

        self.animation_speed = 0.2
        if self.has_sword:
            return Player.A_SWORD_IDLE
        else:
            return Player.A_IDLE

    def update_animation(self):
        self.rect = self.image.get_rect(center=self.hit_box_rect.center)
        self.animation_idx += self.animation_speed
        current_animation_frames = Player.ANIMATIONS[
            self.get_animation_status()]
        if int(self.animation_idx) >= len(current_animation_frames):
            self.animation_idx = 0
            self.animation_done()
            return
        frame = current_animation_frames[int(self.animation_idx)]
        self.image = pygame.transform.flip(frame, True,
                                           False) if self.flip_image else frame

    def animation_done(self):
        if self.sword_attacking:
            self.sword_attacking = False

    def update_action(self):
        if pygame.mouse.get_pressed()[0] and self.sword_attacking == False:
            self.animation_idx = 0
            self.sword_attacking = True

    def update_horizontal_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.flip_image = False
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.flip_image = True
        else:
            self.direction.x = 0

        self.hit_box_rect.x += self.direction.x * self.speed

    def update_vertical_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.direction.y == 0 and self.on_ground:
            self.gravity = -11
        else:
            self.gravity = self.base_gravity

        self.direction.y += self.gravity
        self.hit_box_rect.y += self.direction.y

    def update_movement(self, sprites: list[pygame.sprite.Sprite]):
        self.update_horizontal_movement()
        sprite: pygame.sprite.Sprite
        # Handle horizontal collision
        for sprite in sprites:
            if self.hit_box_rect.colliderect(sprite) and sprite.colliable:
                if self.direction.x > 0:
                    self.hit_box_rect.right = sprite.rect.left
                elif self.direction.x < 0:
                    self.hit_box_rect.left = sprite.rect.right

        self.update_vertical_movement()
        # Handle vertical collision
        for sprite in sprites:
            if sprite.colliable and self.hit_box_rect.colliderect(sprite):
                if self.direction.y > 0:
                    self.hit_box_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hit_box_rect.top = sprite.rect.bottom
                    self.direction.y = 0

        if self.direction.y < 0:
            self.on_ground = False

    def update(self, sprites: list[pygame.sprite.Sprite]):
        self.update_action()
        self.update_movement(sprites)
        self.update_animation()
