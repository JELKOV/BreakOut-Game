class ScoreBoard:
    def __init__(self, font, initial_score=0, initial_lives=3):
        # 점수판 초기화
        self.score = initial_score  # 초기 점수
        self.lives = initial_lives  # 초기 목숨
        self.font = font  # 점수판에 사용할 폰트

    def update(self, score_delta=0, lives_delta=0):
        # 점수와 목숨 업데이트
        self.score += score_delta  # 점수 변경
        self.lives += lives_delta  # 목숨 변경

    def draw(self, screen, level):
        # 점수, 목숨, 레벨 정보를 화면에 표시
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # 점수 텍스트
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))  # 목숨 텍스트
        level_text = self.font.render(f"Level: {level}", True, (255, 255, 255))  # 레벨 텍스트
        # 화면에 텍스트 배치
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))