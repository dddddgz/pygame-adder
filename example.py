from pygame_adder import *
from webbrowser import open as open_webpage

initalize((640, 480))

font30 = pygame.font.SysFont("更纱黑体 SC", 30)
label = Label({}, "欢迎来到 Pygame Adder 的世界", font30, (100, 100), (255, 255, 255))
trace(label)
button = Button({}, "btn1", "开始", font30, (100, 200), (200, 75), (255, 255, 255), (34, 177, 76), lambda: open_webpage("https://github.com/dddddgz/Pygame-Adder/wiki"))
trace(button)
quitbtn = Button({}, "quit", "退出", font30, (320, 200), (200, 75), (255, 255, 255), (32, 64, 255), lambda: (quit(), exit()))
trace(quitbtn)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
quit()
