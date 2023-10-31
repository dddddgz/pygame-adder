from pygame_adder import *

initalize((640, 480))

font30 = pygame.font.SysFont("更纱黑体 SC", 30)
label = Label({}, "欢迎来到 Pygame Adder 的世界", font30, (100, 100), (255, 255, 255))
trace(label)
button = Button({}, "btn1", "开始", font30, (100, 200), (200, 75), (255, 255, 255), (34, 177, 76))
trace(button)
quitbtn = Button({}, "quit", "退出", font30, (320, 200), (200, 75), (255, 255, 255), (32, 64, 255))
trace(quitbtn)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
pygame.quit()
