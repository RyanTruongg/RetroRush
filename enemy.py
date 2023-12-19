import pygame
import entity
import utils


class Enemy(entity.Entity):
    A_IDLE = 'idle'
    A_BEING_ATTACKED = 'being_attacked'

    ANIMATIONS = {
        A_IDLE:
        utils.split_from('graphics/character/idle_48.png', 48, 2),
        A_BEING_ATTACKED:
        utils.split_from('graphics/character/being_attacked_48.png', 48, 2)
    }

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.image = pygame.Surface((32, 64))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center=position)

        self.being_acttacked = False

    def get_animations(self):
        return Enemy.ANIMATIONS

    def get_animation_status(self):
        if self.being_acttacked:
            return Enemy.A_BEING_ATTACKED
        return Enemy.A_IDLE

    def animation_done(self):
        self.being_acttacked = False

    def on_attacked(self):
        self.animation_idx = 0
        self.being_acttacked = True

    def update(self, collidable_sprites: list[pygame.sprite.Sprite]) -> None:
        super().update(collidable_sprites)
        self.rect = self.image.get_rect(center=self.hit_box_rect.center)
