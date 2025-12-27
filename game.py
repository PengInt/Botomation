import pygame, os, platform
#import dotbot
import pathlib as pl
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
	def __init__(this, pos: list, dim: list, parent, c: tuple):
		this.x, this.y = pos
		this.w, this.h = dim
		this.p = parent
		this.c = c
	def draw(this):
		main.ARECT3(this.x + this.p.pos[0], this.y + this.p.pos[1], this.w, this.h, this.c)

class BTN (UI):
	def __init__(this, pos: list, dim: list, parent, c: tuple, effect: str):
		super().__init__(pos, dim, parent, c)
		this.effect = effect
	def onClick(this):
		exec(this.effect, allVars)

class WND: #Window
	windows = []
	tBarh = 30  # Title Bar Height
	tBarp = 4   # Title Bar padding
	@classmethod
	def render(cls):
		for window in cls.windows:
			window.draw()
	def __init__(this, x: float, y: float, w: float, h: float, n: str, i):
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
			BTN(
				[this.size[0]-WND.tBarh+WND.tBarp, WND.tBarp-WND.tBarh],
				[WND.tBarh-WND.tBarp*2, WND.tBarh-WND.tBarp*2],
				this,
				(255, 102, 102),
				f'{this}.close()'
			)
		]
		this.opened = True
		WND.windows.append(this)
	def addUI(this, ui: UI):
		this.UI.append(UI)
	def draw(this):
		main.ARECT3(this.pos[0], this.pos[1], this.size[0], this.size[1], (102, 102, 102))
		for ui in this.UI:
			ui.draw()
	def close(this):
		del this
	def min(this):
		this.opened = False
	def open(this):
		this.opened = True

class FE (WND): #File Explorer
	def __init__(this):
		super().__init__(-80, 45, 160, 90, 'File Explorer', None)
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