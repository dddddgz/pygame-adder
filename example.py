from pygame_adder import *
from webbrowser import open as open_webpage

initalize((640, 480))

def set_rotate(value):
    def inner():
        global rotate
        rotate = value
    return inner

font30 = pygame.font.SysFont("Microsoft YaHei UI", 30)
label = Label({}, "欢迎来到 Pygame Adder 的世界", font30, (310, 100), (255, 255, 255))
trace(label)
button = Button({}, "btn1", "开始", font30, (100, 300), (200, 75), (255, 255, 255), (34, 177, 76), set_rotate(True))
trace(button)
quitbtn = Button({}, "quit", "停止", font30, (320, 300), (200, 75), (255, 255, 255), (255, 32, 24), set_rotate(False))
trace(quitbtn)

clock = pygame.time.Clock()
rotate = False
running = True
while running:
    clock.tick(30)
    if rotate:
        label.rotate(-1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
quit()
