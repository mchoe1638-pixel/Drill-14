from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
COLS, ROWS = 5, 3   # bird_animation.png: 가로 5칸, 세로 3줄


class Bird:
    def __init__(self, x, y):
        self.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        # 시트 크기를 칸 수로 나눠 프레임 1칸 크기 계산
        self.frame_w = self.image.w // COLS
        self.frame_h = self.image.h // ROWS

    def update(self):
        pass

    def draw(self):
        # pico2d는 원점이 왼쪽 아래 → 시트 맨 윗줄은 bottom = frame_h * 2
        self.image.clip_draw(0, self.frame_h * (ROWS - 1),
                             self.frame_w, self.frame_h, self.x, self.y)


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas(CANVAS_W, CANVAS_H)
bird = Bird(400, 300)

running = True
while running:
    handle_events()
    bird.update()
    clear_canvas()
    bird.draw()
    update_canvas()
    delay(0.01)

close_canvas()