import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import ScoreBoard

class Game:
    def __init__(self):
        # 게임 초기화 및 객체 생성
        pygame.init()
        self.screen_info = pygame.display.Info()  # 현재 화면 정보를 가져옴
        self.screen_width = 1680  # 화면 너비
        self.screen_height = 950  # 화면 높이
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # 창 모드
        pygame.display.set_caption("Breakout Game")  # 게임 제목 설정
        self.clock = pygame.time.Clock()  # 프레임 속도 제어
        self.running = True  # 게임 실행 상태

        # 게임 객체 초기화
        self.paddle = Paddle(self.screen_width // 2 - 50, self.screen_height - 40, 100, 10, 7, self.screen_width)  # 패들
        self.ball = Ball(self.screen_width // 2, self.screen_height // 2, 10, 4, -4, self.screen_width, self.screen_height)  # 공
        self.bricks = []  # 벽돌 배열 초기화
        self.font = pygame.font.Font(None, 36)  # 점수판에 사용할 폰트
        self.scoreboard = ScoreBoard(self.font)  # 점수판
        self.level = 1  # 초기 레벨
        self.max_level = 10  # 최대 레벨
        self.initialize_level()  # 레벨 초기화

    def run(self):
        # 게임 루프
        while self.running:
            self.handle_events()  # 사용자 입력 처리
            self.update()  # 게임 상태 업데이트
            self.draw()  # 화면 업데이트
            self.clock.tick(60)  # 60 FPS로 실행

    def handle_events(self):
        # 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 종료 이벤트
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 키로 종료
                    self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # Shift 키를 누르면 패들 속도 증가
            self.paddle.speed = 15
        else:  # 기본 속도
            self.paddle.speed = 7

        if keys[pygame.K_LEFT]:  # 왼쪽으로 이동
            self.paddle.move("LEFT")
        if keys[pygame.K_RIGHT]:  # 오른쪽으로 이동
            self.paddle.move("RIGHT")

    def initialize_level(self):
        # 레벨 초기화
        paddle_width = self.screen_width // 10  # 패들 너비
        paddle_height = self.screen_height // 50  # 패들 높이
        paddle_y = int(self.screen_height * 0.95)  # 패들 위치

        self.paddle = Paddle(
            self.screen_width // 2 - paddle_width // 2,
            paddle_y,
            paddle_width,
            paddle_height,
            7,
            self.screen_width
        )  # 패들 초기화

        self.ball = Ball(
            self.screen_width // 2,
            self.screen_height // 2,
            10,
            4 + self.level,
            -4 - self.level,
            self.screen_width,
            self.screen_height
        )  # 공 초기화 (레벨에 따라 속도 증가)

        # 벽돌 초기화
        rows = 8
        cols = 14
        brick_width = self.screen_width // cols
        brick_height = 30
        spacing = 2

        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                brick_x = col * (brick_width + spacing)
                brick_y = row * (brick_height + spacing)
                color = (100 + col * 10, 50 + row * 20, 150)
                self.bricks.append(
                    Brick(brick_x, brick_y, brick_width - spacing, brick_height - spacing, color)
                )

    def update(self):
        # 게임 상태 업테이트
        self.ball.move()  # 공 이동

        # 공과 충돌 처리
        if self.ball.check_collision(self.paddle, self.bricks):  # 공이 패들 또는 벽돌과 충돌하면
            self.scoreboard.update(score_delta=10)  # 점수 증가

        # 모든 벽돌이 제거되었을 때
        if all(brick.is_destroyed for brick in self.bricks):
            if self.level < self.max_level:  # 다음 레벨로 이동
                self.level += 1
                self.scoreboard.update(lives_delta=1)  # 레벨 클리어 시 목숨 추가
                self.initialize_level()
            else:
                self.running = False  # 최대 레벨 도달 시 게임 종료

        # 공이 화면 하단으로 떨어졌을 때
        if self.ball.y - self.ball.radius > self.screen_height:
            self.scoreboard.update(lives_delta=-1)  # 목숨 감소
            if self.scoreboard.lives <= 0:  # 목숨이 0 이하이면 게임 종료
                self.running = False
            else:
                # 공 초기화
                self.ball = Ball(
                    self.screen_width // 2, self.screen_height // 2, 10, 4 + self.level, -4 - self.level,
                    self.screen_width, self.screen_height
                )

    def draw(self):
        # 게임 화면에 객체 그리기
        self.screen.fill((0, 0, 0))  # 배경을 검은색으로 채움
        self.paddle.draw(self.screen)  # 패들 그리기
        self.ball.draw(self.screen)  # 공 그리기
        for brick in self.bricks:  # 벽돌 그리기
            brick.draw(self.screen)
        self.scoreboard.draw(self.screen, self.level)  # 점수판과 레벨 표시
        pygame.display.flip()  # 화면 업데이트

if __name__ == "__main__":
    game = Game()  # 게임 객체 생성
    game.run()  # 게임 실행
