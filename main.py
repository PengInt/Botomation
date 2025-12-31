#exec(open('dotbot.py', 'r').read())
#exit()
import random, math, pygame, pathlib, game, time

if __name__ == '__main__':
    pygame.init()
    
    info = pygame.display.Info()
    sw, sh = info.current_w, info.current_h
    screen = pygame.display.set_mode((sw, sh), pygame.SCALED | pygame.FULLSCREEN, vsync=1)
    pygame.display.set_caption('Botomation')
    pygame.display.set_icon(pygame.image.load('Images/Roomba.png'))
else:
    screen = None
#game.FE().printCont()
def init(s):
    global screen
    screen = s
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
    if y1 < y2:
        temp = y1
        y1 = y2
        y2 = temp
    pygame.draw.rect(screen, c, (cx+x1*s, cy-y1*s, cx+x2*s, cy-y2*s))
    print((cx+x1*s, cy-y1*s, cx+x2*s, cy-y2*s))
def ARECT3(x: float, y: float, w: float | str, h: float, c: tuple) -> None:
    s = screen.get_height()/1000
    if w == 'window width':
        w = screen.get_width()/s
    pygame.draw.rect(screen, c, (math.floor(x*s), math.floor(y*s), math.ceil(w*s), math.ceil(h*s)))
def AIMG3(x: float, y: float, w: float, h: float, p: pathlib.Path) -> None:
    s = screen.get_height()/1000
    img = pygame.image.load(p)
    img = pygame.transform.scale(img, (math.ceil(w*s), math.ceil(h*s)))
    screen.blit(img, (math.floor(x*s), math.floor(y*s)))
def IMG(x: float, y: float, w: float, h: float, p: pathlib.Path) -> None:
    cx = screen.get_width()/2
    cy = screen.get_height()/2
    s = cy/500
    img = pygame.image.load(p)
    img = pygame.transform.scale(img, (math.ceil(w*s), math.ceil(h*s)))
    screen.blit(img, (math.floor(cx+(x-w/2)*s), math.floor(cy-(y+h/2)*s)))

if __name__ == '__main__':
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
ticking = True

lFT = time.time()
cFT = time.time()
dragging = None
running = True
if __name__ == '__main__':
    game.init(screen)
    game.FE(150, 100, 300, 200)
    game.CE(450, 300, 300, 200, pathlib.Path('SCRIPTS') / '_main_.bot')
    background = pygame.image.load('Images/Wood Grain.png')
    ww, wh = screen.get_size()
    background = pygame.transform.scale(background, (wh/5, wh/5))
    BGCount = (6, math.ceil(5*wh/ww)+1)
    def drawBG():
        for x in range(BGCount[0]):
            for y in range(BGCount[1]):
                screen.blit(background, ((x+game.player.pos[0])*wh/5, (y-game.player.pos[1])*wh/5))
    def drawPlayer():
        IMG(0, 0, wh/5, wh/5, game.player.image)
        for weapon in game.player.weapons:
            if weapon.type == 'flamethrower':
                IMG(0, 0, wh/5, wh/5, pathlib.Path('Images') / 'Flammenwerfer.png')
    while running:
        pygame.display.update()
        cFT = time.time()
        dT = cFT-lFT
        lFT = cFT
        screen.fill((0, 0, 0))
        drawBG()
        drawPlayer()
        game.WND.render()
        game.TB.draw()
        game.HB.draw()
        clickPos = ()
        dp = ()
        initHoldPos = ()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                result = game.MKI(e.key)
                if result == 'menu':
                    paused = not paused
                elif result == 'pause':
                    ticking = not ticking
                elif result == 'FILE EXPLORER':
                    game.FE(random.randint(0, 700), random.randint(0, 700), 300, 200)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    clickPos = e.pos
            elif e.type == pygame.MOUSEMOTION:
                dp = e.rel
                initHoldPos = (e.pos[0] - dp[0], e.pos[1] - dp[1])
        if paused:
            RECT(0, 200, 200, 60, (255, 255, 255))
            TEXT(0, 200, 'RESUME', (0, 0, 0), pathlib.Path('Fonts')/'FiraCode-Regular.ttf', 25)
            if clickPos:
                if CHECKCLICK(0, 200, 200, 60):
                    paused = False
        else:
            if clickPos:
                s = screen.get_height()/1000
                clickPos = (clickPos[0]/s, clickPos[1]/s)
                if len(game.WND.windows):
                    game.TB.checkClicks(clickPos)
                    game.WND.MC(clickPos)
            elif initHoldPos and dp:
                s = screen.get_height()/1000
                initHoldPos = (initHoldPos[0]/s, initHoldPos[1]/s)
                dp = (dp[0]/s, dp[1]/s)
    pygame.quit()