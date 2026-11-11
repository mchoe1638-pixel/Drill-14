import time

running = False
stack = []
frame_time = 0.0


def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.init()

    frame_time = 0.0
    current_time = time.perf_counter()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        now = time.perf_counter()
        frame_time = now - current_time
        current_time = now
        frame_rate = 1.0 / frame_time if frame_time > 0 else 0.0
        print(f'Frame Time : {frame_time:.6f} sec, Frame Rate: {frame_rate:.6f} fps')

    # 루프 종료 시 남은 모드 정리
    while stack:
        stack.pop().finish()


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False