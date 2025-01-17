import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_width):
        # 패들 초기화
        self.x = x  # 패들의 X 좌표
        self.y = y  # 패들의 Y 좌표
        self.width = width  # 패들의 너비
        self.height = height  # 패들의 높이
        self.speed = speed  # 패들의 이동 속도
        self.screen_width = screen_width  # 화면 너비 (경계 처리용)

    def move(self, direction):
        # 패들을 왼쪽 또는 오른쪽으로 이동
        if direction == "LEFT" and self.x > 0:  # 왼쪽 경계 확인
            self.x -= self.speed
        elif direction == "RIGHT" and self.x < self.screen_width - self.width:  # 오른쪽 경계 확인
            self.x += self.speed

    def draw(self, screen):
        # 화면에 패들 그리기
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))
