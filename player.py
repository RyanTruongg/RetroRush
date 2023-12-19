import pygame
from enemy import Enemy
import utils
import entity


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


class Player(entity.Entity):
    jump_frames = utils.split_from('graphics/character/jump_48.png', 48, 2)
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
        utils.split_from('graphics/character/idle_48.png', 48, 2),
        A_SWORD_IDLE:
        utils.split_from('graphics/character/sword/sword_idle_48.png', 48, 2),
        A_RUN:
        utils.split_from('graphics/character/run_48.png', 48, 2),
        A_SWORD_RUN:
        utils.split_from('graphics/character/sword/sword_run_48.png', 48, 2),
        A_JUMP: [jump_frames[0]],
        A_JUMP_MAX: [jump_frames[1]],
        A_FALL: [jump_frames[2]],
        A_SWORD_ATTACK:
        utils.split_from('graphics/character/sword/sword_attack_64.png', 64,
                         2),
    }

    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.effects_group = pygame.sprite.Group()

        self.base_speed = 5
        self.speed = self.base_speed

        self.has_sword = True
        self.attacking = False

        self.image = Player.ANIMATIONS[self.get_animation_status()][0]
        self.rect = self.hit_box_rect.copy()
        self.attack_hit_box_rect = self.hit_box_rect.copy()
        self.attack_hit_box_rect.width = 48

    def get_animations(self):
        return Player.ANIMATIONS

    def get_animation_status(self):
        if self.attacking:
            if self.has_sword:
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

    def animation_done(self):
        if self.attacking:
            self.attacking = False
            self.speed = self.base_speed

    def update_animation(self):
        super().update_animation()
        if self.facing_left:
            self.attack_hit_box_rect.right = self.hit_box_rect.left
        else:
            self.attack_hit_box_rect.left = self.hit_box_rect.right
        self.attack_hit_box_rect.bottom = self.hit_box_rect.bottom

    def handle_attack(self, enemy_sprites: list[Enemy]):
        if pygame.mouse.get_pressed(
        )[0] and self.attacking == False and self.on_ground:
            self.animation_idx = 0
            self.attacking = True
            self.speed = 0

        if self.attacking and int(self.animation_idx) == 2:
            for enemy in enemy_sprites:
                if self.attack_hit_box_rect.colliderect(enemy.hit_box_rect):
                    enemy.on_attacked()

    def update_horizontal_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            if self.attacking != True:
                self.facing_left = False
        elif keys[pygame.K_a]:
            self.direction.x = -1
            if self.attacking != True:
                self.facing_left = True
        else:
            self.direction.x = 0

        self.hit_box_rect.x += self.direction.x * self.speed

    def update_vertical_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.direction.y == 0 and self.on_ground:
            self.gravity = -11
        else:
            self.gravity = self.base_gravity

        super().update_vertical_movement()

    def update(self, collidable_sprites: list[pygame.sprite.Sprite],
               enemy_sprites: list[Enemy]):
        super().update(collidable_sprites)
        self.handle_attack(enemy_sprites)
        self.rect = self.image.get_rect(center=self.hit_box_rect.center)
