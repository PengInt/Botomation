import dotbot
exit()
import pygame, os, platform, math
import pathlib as pl
from termcolor import colored as c
from types import SimpleNamespace as sn
import main

allVars = globals()


screen = None

typing = False

def CC():
	# Check the operating system name
	if platform.system() == "Windows":
		# Command for Windows
		os.system('cls')
	else:
		# Command for Linux and macOS
		os.system('clear')

def init(s):
	global screen
	screen = s
	main.init(screen)
	return

def MKI(key):
	global typing
	if key == pygame.K_1 and not typing:
		return 'FILE EXPLORER'
	elif key == pygame.K_2 and not typing:
		return 'MANAGE WINDOWS'
	elif key == pygame.K_ESCAPE:
		if typing:
			typing = False
			return
		return 'menu'
	elif key == pygame.K_BACKSLASH and not typing:
		return 'menu'
	elif key == pygame.K_p and not typing:
		return 'pause'

class placeHolderParent:
	def __init__(this):
		this.pos = (0, 0)

class UI:
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], parent: object, c: tuple[float, float, float]):
		this.x, this.y = pos
		this.w, this.h = dim
		this.p = parent
		if this.p == None:
			this.p = placeHolderParent()
		this.c = c
	def draw(this):
		main.ARECT3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.c)

class IMG (UI):
	def __draw(this):
		main.AIMG3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.path)
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], parent: object, path: pl.Path):
		super().__init__(pos, dim, parent, (0, 0, 0))
		del this.c
		this.path = path
		this.draw = this.__draw

class BTN (UI):
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], parent: object, c: tuple[float, float, float], callback):
		super().__init__(pos, dim, parent, c)
		this.callback = callback
	def onClick(this):
		this.callback()

class IMGBTN (BTN):
	def __draw(this):
		main.AIMG3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.path)
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], parent: object, path: pl.Path, callback):
		super().__init__(pos, dim, parent, (0, 0, 0), callback)
		del this.c
		this.path = path
		this.draw = this.__draw
	def onClick(this):
		this.callback()

class WND: #Window
	windows = []
	tBarh = 30  # Title Bar Height
	tBarp = 4   # Title Bar padding
	maxWND = 10
	@classmethod
	def TBUpd(cls):
		pass
	@classmethod
	def render(cls):
		for window in cls.windows:
			window.draw()
	@classmethod
	def MC(cls, pos: tuple):
		for wnd in reversed(cls.windows):
			if not wnd.opened:
				continue
			wndA = [wnd.pos[0], wnd.pos[1]-cls.tBarh, wnd.pos[0]+wnd.size[0], wnd.pos[1]+wnd.size[1]]
			x, y = pos
			if wndA[0] <= x <= wndA[2] and wndA[1] <= y <= wndA[3]:
				wnd.sendToFront()
				wnd.checkClicks((x-wnd.pos[0], y-wnd.pos[1]))
				return
	@classmethod
	def MH(cls, pos: tuple, dp: tuple):
		for wnd in reversed(cls.windows):
			if not wnd.opened:
				continue
			wndA = [wnd.pos[0], wnd.pos[1]-cls.tBarh, wnd.pos[0]+wnd.size[0], wnd.pos[1]+wnd.size[1]]
			x, y = pos
			if wndA[0] <= x <= wndA[2] and wndA[1] <= y <= wndA[3]:
				wnd.sendToFront()
				wndA[1] = -cls.tBarh
				if wndA[0] <= x <= wndA[2] and wndA[1] <= y <= wndA[3]:
					wnd.pos[0] += dp[0]
					wnd.pos[1] += dp[1]
					return
				wnd.checkHold((x-wnd.pos[0], y-wnd.pos[1]))
				return
	def __init__(this, x: float, y: float, w: float, h: float, n: str, i: pl.Path):
		if len(WND.windows) >= WND.maxWND:
			print(c('MAX WINDOWS REACHED - DIDN\'T CREATE WINDOW', (255, 0, 0)))
			del this
			return
		this.pos = [x, y]
		this.size = [w, h]
		this.name = n
		this.icon = i
		this.UI = [
			UI(
				[0, -WND.tBarh],
				[this.size[0], WND.tBarh],
				this,
				(204, 204, 204)
			),
			IMG(
				[WND.tBarp+WND.tBarp, WND.tBarp-WND.tBarh],
				[WND.tBarh-WND.tBarp*2, WND.tBarh-WND.tBarp*2],
				this,
				i
			),
			BTN(
				[this.size[0]-WND.tBarh+WND.tBarp, WND.tBarp-WND.tBarh],
				[WND.tBarh-WND.tBarp*2, WND.tBarh-WND.tBarp*2],
				this,
				(255, 102, 102),
				lambda: this.close()
			),
			BTN(
				[this.size[0]-2*WND.tBarh+WND.tBarp, WND.tBarp-WND.tBarh],
				[WND.tBarh-WND.tBarp*2, WND.tBarh-WND.tBarp*2],
				this,
				(255, 204, 51),
				lambda: this.min()
			)
		]
		this.opened = True
		WND.windows.append(this)
		WND.TBUpd()
		#print(c(f'Created Window: {this.name}', (102, 255, 102)))
	def addUI(this, ui: UI):
		this.UI.append(UI)
	def draw(this):
		if this.opened:
			main.ARECT3(this.pos[0], this.pos[1], this.size[0], this.size[1], (102, 102, 102))
			for ui in this.UI:
				ui.draw()
	def close(this):
		WND.windows.remove(this)
		#print(c(f'Closed Window: {this.name}', (255, 102, 102)))
		del this
		WND.TBUpd()
	def min(this):
		this.opened = False
		#print(c(f'Minimised Window: {this.name}', (255, 204, 51)))
	def sendToFront(this):
		#print(c(f'From {WND.windows.index(this)}', (255, 0, 255)), end=' ')
		WND.windows.remove(this)
		WND.windows.append(this)
		#print(c(f'To {WND.windows.index(this)}', (255, 0, 255)))
		WND.TBUpd()
	def open(this):
		this.opened = True
		this.sendToFront()
		#print(c(f'Opened Window: {this.name}', (51, 153, 51)))
	def checkClicks(this, rpos):
		for btn in this.UI:
			if isinstance(btn, BTN):
				btnA = [btn.x, btn.y, btn.x+btn.w, btn.y+btn.h]
				x, y = rpos
				if btnA[0] <= x <= btnA[2] and btnA[1] <= y <= btnA[3]:
					btn.onClick()
	def checkHold(this, rpos):
		pass

class FE (WND): #File Explorer
	def __init__(this, x, y, w, h):
		super().__init__(x, y, w, h, 'File Explorer', pl.Path('Images') / 'Folder.png')
		this.cDir = pl.Path.cwd()
		this.contents = []
		this.getCont()
	def getCont(this):
		this.contents = []
		for i in pl.Path.iterdir(this.cDir):
			this.contents.append(i)
	def printCont(this):
		CC()
		for i in this.contents:
			print(i.name)
		print('BACK: [<]')
		openPath = input('\n  >>> ')
		
		if openPath == '<':
			this.cDir = this.cDir.parent
		else:
			tgt = this.cDir / openPath
			if tgt.is_dir() or tgt.is_file():
				if tgt.is_dir():
					this.cDir = this.cDir / openPath
				else:
					CC()
					print((this.cDir / openPath).read_text('utf-8'))
					input('BACK: [<]  ')
			else:
				input('Invalid path [ENTER]  ')
		this.getCont()
		this.printCont()

class CE (WND): #Code Editor
	def __init__(this, x: float, y: float, w: float, h: float, f: pl.Path):
		super().__init__(x, y, w, h, 'Code Editor', pl.Path('Images') / 'Code Editor.png')
		this.file = f

class TB: #Taskbar
	height = WND.tBarh
	padding = WND.tBarp
	windows = WND.windows
	BTNs = []
	def upd():
		TB.BTNs = []
		for i in range(len(WND.windows)):
			wnd = WND.windows[i]
			TB.BTNs.append(IMGBTN((i*TB.height+TB.padding, 1000-TB.height+TB.padding), (TB.height - TB.padding*2, TB.height - TB.padding*2), None, wnd.icon, lambda w=wnd: w.open()))
	def draw():
		main.ARECT3(0, 1000-TB.height, 'window width', TB.height, (51, 51, 51))
		for x in range(len(TB.BTNs)):
			TB.BTNs[x].draw()
	def checkClicks(rpos):
		for btn in TB.BTNs:
			btnA = [btn.x, btn.y, btn.x+btn.w, btn.y+btn.h]
			x, y = rpos
			if btnA[0] <= x <= btnA[2] and btnA[1] <= y <= btnA[3]:
				btn.onClick()
WND.TBUpd = TB.upd

class GUI:
	def __init__(this, pos: tuple[float, float]):
		this.x, this.y = pos
	def draw(this):
		pass

class RECTGUI (GUI):
	def __draw(this):
		main.ARECT3(this.x, this.y, this.w, this.h, this.c)
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], c: tuple[float, float, float]):
		super().__init__(pos)
		this.w, this.h = dim
		this.c = c
		this.draw = this.__draw

class IMGGUI (GUI):
	def __draw(this):
		main.AIMG3(this.x, this.y, this.w, this.h, this.path)
	def __init__(this, pos: tuple[float, float], dim: tuple[float, float], p: pl.Path):
		super().__init__(pos)
		this.w, this.h = dim
		this.path = p
		this.draw = this.__draw

class HB: #Health Bar
	GUI = [
		IMGGUI((20, 20), (80, 80), pl.Path('Images') / 'Sprocket.png'),
		IMGGUI((60, 40), (40, 40), pl.Path('Images') / 'Full Health Bar Middle.png'),
		IMGGUI((100, 40), (40, 40), pl.Path('Images') / 'Full Health Bar Middle.png'),
		IMGGUI((140, 40), (40, 40), pl.Path('Images') / 'Full Health Bar End.png'),
	]
	def draw():
		for gui in reversed(HB.GUI):
			gui.draw()


class SYS:
	_weapons = []
	@classmethod
	def getWeapons(cls):
		return SYS._weapons
	@classmethod
	def addWeapon(cls, weapon):
		SYS._weapons.append(weapon)
	@classmethod
	def removeWeapon(cls, weapon):
		SYS._weapons.remove(weapon)



try:
	player = dotbot.Variable.variables['PLAYER'].define()
	enemyClass = dotbot.Variable.variables['ENEMY']
except NameError:
	def __getWepons():
		player.weapons = SYS.getWeapons()
	def __takeDamage(this, amt, type):
		this.hp -= amt
	player = sn(
		pos = [0, 0],
		direction = 0,
		hp = 100,
		speed = 2,
		weapons = [sn()],
		takeDamage = __takeDamage,
		behaviours = {
			'Event Listeners': {'weapon': __getWepons}
		}
	)
	SYS.addWeapon(sn(
		type = 'flamethrower',
		fire = sn(
			damage = 2,
			interval = 0.1,
			ease = 0.05
		),
		range = 5,
		magSize = 150,
		fireRate = 30,
		spread = 15,
		speed = 5,
		timeUntilShoot = 0
	))
	def __defineEnemy(difficulty: float, type: str, pos: list[float]):
		if type == 'normal':
			return sn(
				type = type,
				difficulty = difficulty,
				pos = pos,
				direction = 0,
				hp = 100 * difficulty,
				speed = 0.875 + 0.125 * difficulty,
				weapon = sn(
					type = 'fists',
					range = 1.25,
					magSize = 0,
					fireRate = 0.4,
					spread = 0,
					speed = 100,
					timeUntilShoot = 0
				)
			)
	def __enemyAttack(this, target):
		if this.weapon.type == 'fists' and ((target.pos[0] - this.pos[0])**2 + (target.pos[1] - this.pos[1])**2) ** 0.5 <= this.weapon.range:
			target.takeDamage(5, 'physical')
	enemyClass = sn(define = __defineEnemy, ATTACK = __enemyAttack)
	del __takeDamage
	del __defineEnemy
	del __enemyAttack
	del __getWepons

player.image = pl.Path('Images') / 'Roomba.png'
player.behaviours['Event Listeners']['weapon']()