import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.on_ground = False

        self.direction = pygame.math.Vector2()
        self.base_gravity = 0.6
        self.gravity = self.base_gravity

        self.hit_box_rect = pygame.Rect(position[0], position[1], 32, 64)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hit_box_rect.y += self.direction.y

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

    def update(self, collidable_sprites: list[pygame.sprite.Sprite]):
        self.apply_gravity()
        self.handle_vertical_collision(collidable_sprites)
