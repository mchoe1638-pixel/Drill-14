from pico2d import load_image

COLS, ROWS = 5, 3   # 스프라이트 시트: 가로 5칸, 세로 3줄


class Bird:
    def __init__(self, x=400, y=400):
        self.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        # 시트 크기를 칸 수로 나눠 프레임 1칸의 크기를 계산
        self.frame_w = self.image.w // COLS
        self.frame_h = self.image.h // ROWS

    def update(self):
        pass

    def draw(self):
        # pico2d는 좌표 원점이 '왼쪽 아래'이므로 맨 윗줄은 bottom = frame_h * 2
        self.image.clip_draw(0, self.frame_h * (ROWS - 1),
                             self.frame_w, self.frame_h, self.x, self.y)