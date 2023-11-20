from pygame_adder import *
from webbrowser import open as open_webpage

initalize((640, 480))

def set_rotate(value):
    def inner():
        global rotate
        rotate = value
    return inner

font30 = pygame.font.SysFont("更纱黑体 SC", 30)
label = Label({}, "欢迎来到 Pygame Adder 的世界", font30, (310, 100), (255, 255, 255))
button = Button({}, "开始", font30, (100, 300), (200, 75), (255, 255, 255), (34, 177, 76), set_rotate(True))
button.right_menu = [("执行函数", button._func)]
quitbtn = Button({}, "停止", font30, (320, 300), (200, 75), (255, 255, 255), (255, 32, 24), set_rotate(False))
quitbtn.right_menu = [("执行函数", quitbtn._func)]
trace(label)
trace(button)
trace(quitbtn)

clock = pygame.time.Clock()
rotate = False
running = True
while running:
    clock.tick(30)
    if rotate:
        label.rotate(-2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
quit()
