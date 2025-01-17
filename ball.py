import pygame

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, screen_width, screen_height):
        # 공 초기화
        self.x = x  # 공의 X 좌표
        self.y = y  # 공의 Y 좌표
        self.radius = radius  # 공의 반지름
        self.speed_x = speed_x  # X축 속도
        self.speed_y = speed_y  # Y축 속도
        self.screen_width = screen_width  # 화면 너비
        self.screen_height = screen_height  # 화면 높이

    def move(self):
        # 공 이동 및 화면 경계 충돌 처리
        self.x += self.speed_x
        self.y += self.speed_y

        # 왼쪽, 오른쪽 경계 충돌
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x = -self.speed_x
        if self.x + self.radius >= self.screen_width:
            self.x = self.screen_width - self.radius
            self.speed_x = -self.speed_x

        # 상단 경계 충돌
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = -self.speed_y

    def check_collision(self, paddle, bricks):
        """공과 패들 및 벽돌의 충돌 처리"""
        # 패들과 충돌
        if (
                self.y + self.radius >= paddle.y and
                paddle.x <= self.x <= paddle.x + paddle.width
        ):
            self.y = paddle.y - self.radius
            self.speed_y = -abs(self.speed_y)

        # 벽돌과 충돌
        for brick in bricks:
            if not brick.is_destroyed and (
                    brick.x <= self.x <= brick.x + brick.width and
                    brick.y <= self.y <= brick.y + brick.height
            ):
                brick.hit()
                self.speed_y = -self.speed_y
                return brick  # 충돌한 벽돌 반환
        return None  # 충돌한 벽돌이 없는 경우


    def draw(self, screen):
        # 화면에 공 그리기
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
