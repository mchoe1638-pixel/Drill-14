import random
from pico2d import load_image, get_canvas_width, get_canvas_height
import game_framework

COLS, ROWS = 5, 3

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 20.0
FLY_SPEED_MPS = FLY_SPEED_KMPH * 1000.0 / 3600.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER

DRAW_SCALE = 0.5


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.frame_w = Bird.image.w // COLS
        self.frame_h = Bird.image.h // ROWS
        self.draw_w = self.frame_w * DRAW_SCALE
        self.draw_h = self.frame_h * DRAW_SCALE

        cw, ch = get_canvas_width(), get_canvas_height()
        self.x = random.uniform(self.draw_w, cw - self.draw_w)
        self.y = random.uniform(ch * 0.5, ch - self.draw_h)   # 화면 위쪽 절반에서 비행
        self.dir = random.choice([-1, 1])
        self.speed = FLY_SPEED_PPS * random.uniform(0.8, 1.2)
        self.frame = random.uniform(0, FRAMES_PER_ACTION)

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

        self.x += self.dir * self.speed * dt

        half = self.draw_w / 2
        cw = get_canvas_width()
        if self.x > cw - half:
            self.x = cw - half
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