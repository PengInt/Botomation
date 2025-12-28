import pygame, os, platform
#import dotbot
import pathlib as pl
from termcolor import colored as c
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

class UI:
	def __init__(this, pos: list, dim: list, parent: object, c: tuple):
		this.x, this.y = pos
		this.w, this.h = dim
		this.p = parent
		this.c = c
	def draw(this):
		main.ARECT3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.c)

class IMG (UI):
	def __draw(this):
		main.AIMG3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.path)
	def __init__(this, pos: list, dim: list, parent: object, path: pl.Path):
		super().__init__(pos, dim, parent, (0, 0, 0))
		del this.c
		this.path = path
		this.draw = this.__draw

class BTN (UI):
	def __init__(this, pos: list, dim: list, parent: object, c: tuple, callback):
		super().__init__(pos, dim, parent, c)
		this.callback = callback
	def onClick(this):
		this.callback()

class IMGBTN (BTN):
	def __draw(this):
		main.AIMG3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.path)
	def __init__(this, pos: list, dim: list, parent: object, path: pl.Path, callback):
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
				wnd.checkClicks((x-wnd.pos[0], y-wnd.pos[1]))
				return
	def __init__(this, x: float, y: float, w: float, h: float, n: str, i: pl.Path):
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
		print(c(f'Created Window: {this.name}', (102, 255, 102)))
	def addUI(this, ui: UI):
		this.UI.append(UI)
	def draw(this):
		if this.opened:
			main.ARECT3(this.pos[0], this.pos[1], this.size[0], this.size[1], (102, 102, 102))
			for ui in this.UI:
				ui.draw()
	def close(this):
		WND.windows.remove(this)
		print(c(f'Closed Window: {this.name}', (255, 102, 102)))
		del this
	def min(this):
		this.opened = False
		print(c(f'Minimised Window: {this.name}', (255, 204, 51)))
	def sendToFront(this):
		WND.windows.remove(this)
		WND.windows.append(this)
	def open(this):
		this.opened = True
		this.sendToFront()
		print(c(f'Opened Window: {this.name}', (153, 51, 51)))
	def checkClicks(this, rpos):
		for btn in this.UI:
			if isinstance(btn, BTN):
				btnA = [btn.x, btn.y, btn.x+btn.w, btn.y+btn.h]
				x, y = rpos
				if btnA[0] <= x <= btnA[2] and btnA[1] <= y <= btnA[3]:
					btn.onClick()

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