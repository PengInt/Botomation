import pygame, dotbot, os, platform
import pathlib as pl

pygame.init()

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

class WND: #Window
	def __init__(this, x: float, y: float, w: float, h: float, n: str, i):
		this.pos = [x, y]
		this.size = [w, h]
		this.name = n
		this.icon = i
		this.UI = []
	def addUI(this, x, y, w, h, c):
		this.UI.append([[x, y], [w, h]])

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