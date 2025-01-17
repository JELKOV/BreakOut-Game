import pygame

class Brick:
    def __init__(self, x, y, width, height, color):
        # 벽돌 초기화
        self.x = x  # 벽돌 X 좌표
        self.y = y  # 벽돌 Y 좌표
        self.width = width  # 벽돌 너비
        self.height = height  # 벽돌 높이
        self.color = color  # 벽돌 색상
        self.is_destroyed = False  # 벽돌 파괴 여부

    def hit(self):
        # 벽돌이 맞으면 파괴 상태로 변경
        self.is_destroyed = True

    def draw(self, screen):
        # 벽돌이 파괴되지 않았으면 화면에 그리기
        if not self.is_destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
