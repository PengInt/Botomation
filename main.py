import random, pygame, pathlib

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
pygame.display.set_caption('Botomation')
pygame.display.set_icon(pygame.image.load('Images/Roomba.png'))


clickPos = ()

def RECT(x: float, y: float, w: float, h: float, c: tuple) -> None:
    cx = screen.get_width()/2
    cy = screen.get_height()/2
    s = cy/500
    pygame.draw.rect(screen, c, (cx+x*s-w*s/2, cy-y*s-h*s, w*s, h*s))
def RECT2(x1: float, y1: float, x2: float, y2: float, c: tuple) -> None:
    cx = screen.get_width()/2
    cy = screen.get_height()/2
    s = cy/500
    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp
    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp
    pygame.draw.rect(screen, c, (cx+x1*s, cy-y1*s, cx+x2*s, cy-y2*s))

pygame.font.init()
def TEXT(x: float, y: float, t: str, c: tuple, f: pathlib.Path, p: float) -> None:
    cx = screen.get_width() / 2
    cy = screen.get_height() / 2
    s = cy / 500
    font = pygame.font.Font(f, round(p*s))
    text = font.render(t, 1, c)
    w, h = text.get_width(), font.get_ascent()
    pygame.draw.rect(screen, (255, 0, 0), (cx+x*s-w/2, cy-y*s-h/2, w, h))
    screen.blit(text, (cx+x*s-w/2, cy-y*s-h/2))

def CHECKCLICK(x, y, w, h):
    if len(clickPos) == 0:
        return False
    cx = screen.get_width()/2
    cy = screen.get_height()/2
    px = clickPos[0]
    py = clickPos[1]
    s = cy/500
    lmxmin = cx+x*s-w*s/2
    lmxmax = lmxmin+w*s
    lmymin = cy-y*s-h*s
    lmymax = lmymin+h*s
    if (px > lmxmin and px < lmxmax and py > lmymin and py < lmymax):
        return True
    else:
        return False

paused = False

running = True
while running:
    pygame.display.update()
    screen.fill((0, 0, 0))
    clickPos = ()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                paused = not paused
        elif e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            clickPos = pygame.mouse.get_pos()
    if paused:
        RECT(0, 200, 200, 60, (255, 255, 255))
        TEXT(0, 200, 'RESUME', (0, 0, 0), None, 25)#pathlib.Path('Fonts')/'FiraCode-Regular.ttf', 25)
        if len(clickPos) != 0:
            if CHECKCLICK(0, 200, 200, 60):
                paused = False
    else:
        pass    # code to run normally
pygame.quit()