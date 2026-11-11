from pico2d import *
import time
import random

CANVAS_W, CANVAS_H = 800, 600
COLS, ROWS = 5, 3

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 20.0
FLY_SPEED_MPS = FLY_SPEED_KMPH * 1000.0 / 3600.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER

DRAW_SCALE = 0.5
BIRD_COUNT = 10


class Bird:
    image = None   # 모든 새가 이미지 1장을 공유 (클래스 변수)

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.frame_w = Bird.image.w // COLS
        self.frame_h = Bird.image.h // ROWS
        self.draw_w = self.frame_w * DRAW_SCALE
        self.draw_h = self.frame_h * DRAW_SCALE

        # 새마다 위치/방향/속도/시작 프레임을 다르게 → 자연스러운 새떼
        self.x = random.uniform(self.draw_w, CANVAS_W - self.draw_w)
        self.y = random.uniform(self.draw_h, CANVAS_H - self.draw_h)
        self.dir = random.choice([-1, 1])
        self.speed = FLY_SPEED_PPS * random.uniform(0.8, 1.2)
        self.frame = random.uniform(0, FRAMES_PER_ACTION)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                      * frame_time) % FRAMES_PER_ACTION

        self.x += self.dir * self.speed * frame_time

        half = self.draw_w / 2
        if self.x > CANVAS_W - half:
            self.x = CANVAS_W - half
            self.dir = -1
        elif self.x < half:
            self.x = half
            self.dir = 1

    def draw(self):
        f = int(self.frame)
        col, row = f % COLS, f // COLS
        left = col * self.frame_w
        bottom = (ROWS - 1 - row) * self.frame_h

        if self.dir == 1:
            Bird.image.clip_draw(left, bottom, self.frame_w, self.frame_h,
                                 self.x, self.y, self.draw_w, self.draw_h)
        else:
            Bird.image.clip_composite_draw(left, bottom, self.frame_w, self.frame_h,
                                           0, 'h', self.x, self.y,
                                           self.draw_w, self.draw_h)


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas(CANVAS_W, CANVAS_H)
birds = [Bird() for _ in range(BIRD_COUNT)]

running = True
frame_time = 0.0
current_time = time.time()
while running:
    handle_events()
    for bird in birds:
        bird.update()
    clear_canvas()
    for bird in birds:
        bird.draw()
    update_canvas()

    frame_time = time.time() - current_time
    current_time += frame_time

close_canvas()