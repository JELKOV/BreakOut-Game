import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import ScoreBoard
from item import Item
import random

class Game:
    def __init__(self):
        # 게임 초기화 및 객체 생성
        pygame.init()
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
        self.state = "START" # 초기 상태: 게임 시작 화면
        self.items = []  # 화면에 나타나는 아이템 관리

        # 효과 메시지 초기화
        self.effect_message = None  # 현재 표시 중인 효과 메시지
        self.effect_message_timer = 0  # 효과 메시지 표시 타이머

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
                if event.key == pygame.K_ESCAPE:  # ESC 키로 게임 종료
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.state == "START":  # 시작 화면에서 SPACE 키
                        self.state = "RUNNING"  # 게임 시작
                    elif self.state == "LEVEL_COMPLETE":  # 레벨 완료 상태에서 SPACE 키
                        self.state = "RUNNING"
                        self.initialize_level()  # 다음 레벨로 이동

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
        )  # 공 초기화

        rows = 8
        cols = 14
        brick_width = self.screen_width // cols
        brick_height = 30
        spacing = 2

        self.bricks = []
        self.items = []  # 아이템 초기화

        for row in range(rows):
            for col in range(cols):
                brick_x = col * (brick_width + spacing)
                brick_y = row * (brick_height + spacing)
                color = (100 + col * 10, 50 + row * 20, 150)

                self.bricks.append(
                    Brick(brick_x, brick_y, brick_width - spacing, brick_height - spacing, color)
                )

                # 모든 벽돌에 대해 아이템 생성
                if random.random() < 0.2:  # 30% 확률로 아이템 생성
                    item_effect = random.choice(["extra_life", "expand_paddle"])  # 랜덤 효과 선택
                    item_color = (0, 255, 0) if item_effect == "expand_paddle" else (255, 0, 0)  # 색상 결정
                    item = Item(brick_x + brick_width // 4, brick_y + brick_height // 4, 20, 20, 3, item_color,
                                item_effect)
                    self.items.append(item)
                    print(f"Item created at ({item.x}, {item.y}) with effect: {item.effect}")

    def show_effect_message(self, message):
        """아이템 효과 메시지 설정"""
        self.effect_message = message  # 효과 메시지 저장
        self.effect_message_timer = pygame.time.get_ticks() + 1000  # 1초 동안 표시

    def update(self):
        # 게임 상태 업데이트
        self.ball.move()  # 공 이동

        # 공과 벽돌 충돌 처리
        collided_brick = self.ball.check_collision(self.paddle, self.bricks)
        if collided_brick:  # 충돌한 벽돌이 있을 경우
            self.scoreboard.update(score_delta=10)  # 점수 증가

            # 아이템 생성 (랜덤 확률)
            if random.random() < 0.3:  # 30% 확률로 아이템 생성
                item_x = collided_brick.x + collided_brick.width // 2 - 10  # 벽돌 중심
                item_y = collided_brick.y + collided_brick.height  # 벽돌 아래쪽
                item_effect = random.choice(["extra_life", "expand_paddle"])  # 랜덤 효과
                item_color = (0, 255, 0) if item_effect == "expand_paddle" else (255, 0, 0)  # 색상 결정
                new_item = Item(item_x, item_y, 20, 20, 3, item_color, item_effect)
                self.items.append(new_item)
                print(f"Item created at ({new_item.x}, {new_item.y}) due to brick break.")

        # 모든 벽돌이 제거되었을 때
        if all(brick.is_destroyed for brick in self.bricks):
            if self.level < self.max_level:  # 다음 레벨로 이동
                self.level += 1
                self.scoreboard.update(lives_delta=1)  # 레벨 클리어 시 목숨 추가
                self.state = "LEVEL_COMPLETE"  # 상태를 레벨 완료로 변경
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

        # 아이템 이동 및 충돌 처리
        for item in self.items[:]:  # 리스트 복사본으로 반복
            item.move()  # 아이템 이동
            if item.y > self.screen_height:  # 화면 하단을 벗어나면
                self.items.remove(item)  # 리스트에서 제거
            elif item.check_collision(self.paddle):  # 패들과 충돌 확인
                print(f"Item collided with paddle: ({item.x}, {item.y}) - Effect: {item.effect}")
                if item.effect == "extra_life":  # 목숨 추가
                    self.scoreboard.update(lives_delta=1)
                    self.show_effect_message("Extra Life!")
                elif item.effect == "expand_paddle":  # 패들 크기 확장
                    if self.paddle.width < self.screen_width // 2:  # 패들이 너무 크지 않도록 제한
                        self.paddle.width *= 1.5
                        self.show_effect_message("Paddle Expanded!")
                    else:
                        self.show_effect_message("Paddle at Max Size!")  # 최대 크기 도달 메시지 표시
                self.items.remove(item)  # 충돌한 아이템 제거

    def draw_start_screen(self):
        self.screen.fill((0, 0, 0))  # 검은 배경
        title = self.font.render("Breakout Game", True, (255, 255, 255))
        instruction = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        key_guide = self.font.render("Left/Right: Move | Shift: Speed | ESC: Quit", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 200))
        self.screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 300))
        self.screen.blit(key_guide, (self.screen_width // 2 - key_guide.get_width() // 2, 400))
        pygame.display.flip()

    def draw_level_complete_screen(self):
        # 화면 배경 초기화
        self.screen.fill((0, 0, 0))  # 검은 배경

        # 메시지 렌더링
        level_complete_text = self.font.render(f"Level {self.level} Complete!", True, (255, 255, 255))
        next_level_text = self.font.render("Press SPACE to Continue", True, (255, 255, 255))

        # 텍스트를 화면 중앙에 배치
        self.screen.blit(level_complete_text, (self.screen_width // 2 - level_complete_text.get_width() // 2, 300))
        self.screen.blit(next_level_text, (self.screen_width // 2 - next_level_text.get_width() // 2, 400))

        # 화면 업데이트
        pygame.display.flip()

    def draw(self):
        # 게임 화면에 객체 그리기
        if self.state == "START":
            self.draw_start_screen()  # 시작 화면 그리기
        elif self.state == "LEVEL_COMPLETE":
            self.draw_level_complete_screen()  # 레벨 완료 화면 그리기
        else:
            self.screen.fill((0, 0, 0))  # 배경을 검은색으로 채움
            self.paddle.draw(self.screen)  # 패들 그리기
            self.ball.draw(self.screen)  # 공 그리기
            for brick in self.bricks:  # 벽돌 그리기
                brick.draw(self.screen)
            for item in self.items:  # 아이템 그리기
                item.draw(self.screen)
            self.scoreboard.draw(self.screen, self.level)  # 점수판과 레벨 표시

            # 효과 메시지 표시
            if self.effect_message and pygame.time.get_ticks() < self.effect_message_timer:
                effect_text = self.font.render(self.effect_message, True, (255, 255, 255))  # 흰색 텍스트
                self.screen.blit(effect_text,
                                 (self.screen_width // 2 - effect_text.get_width() // 2, self.screen_height // 2))
            else:
                self.effect_message = None  # 메시지가 만료되면 제거

            pygame.display.flip()  # 화면 업데이트

if __name__ == "__main__":
    game = Game()  # 게임 객체 생성
    game.run()  # 게임 실행