import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.animation_idx = 0
        self.animation_speed = 0.2
        self.facing_left = False

        self.on_ground = False

        self.direction = pygame.math.Vector2()
        self.base_gravity = 0.6
        self.gravity = self.base_gravity

        self.hit_box_rect = pygame.Rect(position[0], position[1], 32, 64)

    def get_animations(self):
        pass

    def get_animation_status(self):
        pass

    def animation_done(self):
        pass

    def update_animation(self):
        self.animation_idx += self.animation_speed
        current_animation_frames = self.get_animations()[
            self.get_animation_status()]
        if int(self.animation_idx) >= len(current_animation_frames):
            self.animation_idx = 0
            self.animation_done()
            return
        frame = current_animation_frames[int(self.animation_idx)]
        self.image = pygame.transform.flip(
            frame, True, False) if self.facing_left else frame

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hit_box_rect.y += self.direction.y

    def update_horizontal_movement(self):
        pass

    def handle_horizontal_collision(
            self, collidable_sprites: list[pygame.sprite.Sprite]):
        for sprite in collidable_sprites:
            if self.hit_box_rect.colliderect(sprite) and sprite.colliable:
                if self.direction.x > 0:
                    self.hit_box_rect.right = sprite.rect.left
                elif self.direction.x < 0:
                    self.hit_box_rect.left = sprite.rect.right

    def update_vertical_movement(self):
        self.apply_gravity()

    def handle_vertical_collision(
            self, collidable_sprites: list[pygame.sprite.Sprite]):
        for sprite in collidable_sprites:
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

    def update_movement(self, collidable_sprites: list[pygame.sprite.Sprite]):
        self.update_horizontal_movement()
        self.handle_horizontal_collision(collidable_sprites)
        self.update_vertical_movement()
        self.handle_vertical_collision(collidable_sprites)

    def update(self, collidable_sprites: list[pygame.sprite.Sprite]):
        self.update_movement(collidable_sprites)
        self.update_animation()
