from pygame_adder import *

initalize((640, 480))

font20 = Font("sarasa-mono-sc-regular.ttf", 20, fgcolor=(255, 255, 255))
label = Label({}, "say hello to pygame adder", font20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    flush()
pygame.quit()
