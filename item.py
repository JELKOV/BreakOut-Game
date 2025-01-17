import pygame


class Item:
    def __init__(self, x, y, width, height, speed, color, effect):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.effect = effect
        self.active = True # 아이템 활성화 상태

    def move(self):
        # 아이템 이동
        self.y += self.speed

    def draw(self, screen):
        # 아이템 그리기
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, paddle):
        """패들과의 충돌 확인"""
        if (
                self.active and
                self.y + self.height >= paddle.y and
                paddle.x <= self.x <= paddle.x + paddle.width
        ):
            self.active = False  # 아이템 비활성화
            return True  # 충돌 발생
        return False