from pygame_adder import *

initalize((640, 480))

font20 = pygame.font.SysFont("更纱黑体", 20)
label = Label({}, "Hello World", font20, (100, 100), (255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
pygame.quit()
