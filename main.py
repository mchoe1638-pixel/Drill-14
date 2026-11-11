from pico2d import *
import time

CANVAS_W, CANVAS_H = 800, 600
COLS, ROWS = 5, 3

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

# 10 pixel = 30 cm
PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 20.0
FLY_SPEED_MPS = FLY_SPEED_KMPH * 1000.0 / 3600.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER


class Bird:
    def __init__(self, x, y):
        self.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame_w = self.image.w // COLS
        self.frame_h = self.image.h // ROWS
        self.frame = 0.0
        self.dir = 1   # 1: 오른쪽, -1: 왼쪽

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                      * frame_time) % FRAMES_PER_ACTION

        self.x += self.dir * FLY_SPEED_PPS * frame_time

        half = self.frame_w / 2
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
        self.image.clip_draw(left, bottom, self.frame_w, self.frame_h,
                             self.x, self.y)


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
frame_time = 0.0
current_time = time.time()
while running:
    handle_events()
    bird.update()
    clear_canvas()
    bird.draw()
    update_canvas()

    frame_time = time.time() - current_time
    current_time += frame_time

close_canvas()