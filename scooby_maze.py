#!/usr/bin/env python3
## Copyright (c) 2023, Daniel Tabor
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
## 
## 1. Redistributions of source code must retain the above copyright notice, this
##    list of conditions and the following disclaimer.
## 
## 2. Redistributions in binary form must reproduce the above copyright notice,
##    this list of conditions and the following disclaimer in the documentation
##    and/or other materials provided with the distribution.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
## FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
## CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
## OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import pygame
from pygame.locals import *
import threading
import os
import sys
import random
import time

FRAMES_PER_SECOND = 60

def load_image(filename,bColorkey=True):
	image = None
	full_filename = os.path.join("data",filename)
	try:
		image = pygame.image.load(full_filename)
	except pygame.error as msg:
		raise Exception(msg)
	if bColorkey:
		image = image.convert()
		image.set_colorkey(0xff0000,RLEACCEL)
	return image
    
up_cursor_size = (16,16)
up_cursor_hotspot = (7,15)
up_cursor_strings = (
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"       XX       ",
	"     XX..XX     ",
	"   XX......XX   ",
	" XX..........XX ",
	"XXXXXXX..XXXXXXX",
	"      X..X      ",
	"      X..X      ",
	"      X..X      ",
	"      XXXX      ",
)

down_cursor_size = (16,16)
down_cursor_hotspot = (7,0)
down_cursor_strings = (
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"                ",
	"      XXXX      ",
	"      X..X      ",
	"      X..X      ",
	"      X..X      ",
	"XXXXXXX..XXXXXXX",
	" XX..........XX ",
	"   XX......XX   ",
	"     XX..XX     ",
	"       XX       ",
)

left_cursor_size = (16,16)
left_cursor_hotspot = (15,7)
left_cursor_strings = (
	"           X    ",
	"          XX    ",
	"          XX    ",
	"         X.X    ",
	"         X.X    ",
	"        X..X    ",
	"        X..XXXXX",
	"       X.......X",
	"       X.......X",
	"        X..XXXXX",
	"        X..X    ",
	"         X.X    ",
	"         X.X    ",
	"          XX    ",
	"          XX    ",
	"           X    ",
)

right_cursor_size = (16,16)
right_cursor_hotspot = (0,7)
right_cursor_strings = (
	"    X           ",
	"    XX          ",
	"    XX          ",
	"    X.X         ",
	"    X.X         ",
	"    X..X        ",
	"XXXXX..X        ",
	"X.......X       ",
	"X.......X       ",
	"XXXXX..X        ",
	"    X..X        ",
	"    X.X         ",
	"    X.X         ",
	"    XX          ",
	"    XX          ",
	"    X           ",
)

center_cursor_size = (8,8)
center_cursor_hotspot = (3,3)
center_cursor_strings = (
	"        ",
	"   XX   ",
	"  X..X  ",
	" X....X ",
	" X....X ",
	"  X..X  ",
	"   XX   ",
	"        ",
)  

class MazeObject(pygame.sprite.Sprite):
	CONST = 0x00001
	FRONT = 0x00010
	BACK  = 0x00100
	LEFT  = 0x01000
	RIGHT = 0x10000

	D_UP	= 0
	D_DOWN  = 1
	D_LEFT  = 2
	D_RIGHT = 3
	def __init__(self,name="",demo=None):
		pygame.sprite.Sprite.__init__(self)
		if demo == None:
			self.image = None
			self.direction = None
			self.style = 0
			self.images = {}
			for img_type,name_ext,dir in [(self.BACK,"_back.bmp",self.D_UP),
											(self.LEFT,"_left.bmp",self.D_LEFT),
											(self.RIGHT,"_right.bmp",self.D_RIGHT),
											(self.FRONT,"_front.bmp",self.D_DOWN),
											(self.CONST,".bmp",self.D_DOWN)]:
				try:
					self.images[img_type] = load_image(str(name)+name_ext)
				except Exception as msg:
					pass
				else:
					self.style = self.style | img_type
					self.image = self.images[img_type]
					self.direction = dir
			if self.image == None:
				raise SystemExit("Could not create object \'%s\'" % str(name))
			else:
				width, height = self.image.get_size()
				self.maze_rect = pygame.Rect(0,0,width,height)
				self.rect	  = pygame.Rect(0,0,width,height)
				self.tmp_rect  = pygame.Rect(0,0,0,0)
		else:
			self.style     = demo.style
			self.images    = demo.images
			self.image     = demo.image
			self.direction = demo.direction
			self.maze_rect = pygame.Rect(demo.maze_rect)
			self.rect      = pygame.Rect(demo.rect)
			self.tmp_rect  = pygame.Rect(0,0,0,0)

	def GetMaxSize(self):
		max_width = 0
		max_height = 0
		for img_type in self.images.keys():
			width, height = self.images[img_type].get_size()
			if width > max_width:
				max_width = width
			if height > max_height:
				max_height = height
		return (max_width, max_height)
		
	def GetDirection(self):
		return self.direction

	def CenterOn(self,target_rect):
		self.maze_rect.center = target_rect.center
		
	def Move(self,maze,x_offset,y_offset):
		if not(x_offset == 0 and y_offset == 0):
			if y_offset > 0:
				self.direction = self.D_DOWN
			elif y_offset < 0:
				self.direction = self.D_UP
			if x_offset > 0:
				self.direction = self.D_RIGHT
			elif x_offset < 0:
				self.direction = self.D_LEFT
				
			if not self.style & self.CONST:
				if self.direction == self.D_DOWN and self.style & self.FRONT:
					self.image = self.images[self.FRONT]
				elif self.direction == self.D_UP and self.style & self.BACK:
					self.image = self.images[self.BACK]
				
				if self.direction == self.D_RIGHT and self.style & self.RIGHT:
					self.image = self.images[self.RIGHT]
				elif self.direction == self.D_LEFT and self.style & self.LEFT:
					self.image = self.images[self.LEFT]
				
				self.rect.size	  = self.image.get_size()
				self.maze_rect.size = self.image.get_size()
			
			new_rect = self.tmp_rect
			new_rect.size = self.maze_rect.size
			
			final_x_offset = 0
			for i in range(abs(x_offset)):
				i = i+1
				if x_offset < 0:
					i = 0 - i
				new_rect.topleft = (self.maze_rect.left + i,
									self.maze_rect.top)
				if maze.Collide(new_rect):
					break
				else:
					final_x_offset = i
			self.maze_rect.left = self.maze_rect.left + final_x_offset
	
			final_y_offset = 0
			for i in range(abs(y_offset)):
				i = i+1
				if y_offset < 0:
					i = 0 - i
				new_rect.topleft = ( self.maze_rect.left,
									 self.maze_rect.top + i)
				if maze.Collide(new_rect):
					break
				else:
					final_y_offset = i
			self.maze_rect.top = self.maze_rect.top + final_y_offset
				
	def SetPosition(self,x,y):
		self.maze_rect.left = x
		self.maze_rect.top  = y
		
	def GetPosition(self):
		return self.maze_rect.center

	def GetMazeRect(self):
		return self.maze_rect

	def update(self,view_rect):
		self.rect.left = self.maze_rect.left - view_rect.left
		self.rect.top  = self.maze_rect.top - view_rect.top
		
	def Attack(self,maze,target,speed):
		t_xpos, t_ypos = target.GetPosition()
		x_offset = t_xpos - self.maze_rect.centerx
		y_offset = t_ypos - self.maze_rect.centery
		if abs(x_offset) > speed:
			if x_offset < 0:
				x_offset = 0-speed
			else:
				x_offset = speed
		if abs(y_offset) > speed:
			if y_offset < 0:
				y_offset = 0-speed
			else:
				y_offset = speed
		self.Move(maze,x_offset,y_offset)
		
class Maze:
	NORTH   = 0
	SOUTH   = 1
	EAST	= 2
	WEST	= 3
	VISITED = 4
	
	def __init__(self,num_cols,num_rows,
				 cell_width,cell_height,wall_width):
		#Generate the maze structures
		self.num_rows = num_rows
		self.num_cols = num_cols

		self.cells = []
		for r in range(num_rows):
			row = []
			for c in range(num_cols):
				row.append( [False,False,False,False,False] )
			self.cells.append(row)
		
		self.start_cells = [ (int(num_rows/2),int(num_cols/2)) ]
		while len(self.start_cells) > 0:
			row, col = self.start_cells[0]
			del self.start_cells[0] 
			self._discover(row, col)
			
		#Generate rectangles used to detect collisions
		#and surface used for painting
		self.rects = []
		for c in range(num_cols):
			col = []
			for r in range(num_rows):
				col.append([])
			self.rects.append(col)

		self.cell_width  = cell_width
		self.cell_height = cell_height
		self.wall_width  = wall_width
		self.total_cell_width = cell_width+2*wall_width
		self.total_cell_height = cell_height+2*wall_width
		
		width  = self.total_cell_width*num_cols
		height = self.total_cell_height*num_rows
		self.maze_rect = pygame.Rect(0,0,width,height)

		for r in range(num_rows):
			for c in range(num_cols):
				cell = self.cells[r][c]

				if r == 0:
					if not cell[self.NORTH]:
						rect = (c*self.total_cell_width,
								r*self.total_cell_height,
								self.total_cell_width,
								wall_width)
						self.rects[c][r].append(rect)
				if c == num_cols-1:
					if not cell[self.EAST]:
						rect = ((c+1)*self.total_cell_width - wall_width,
								r*self.total_cell_height,
								wall_width,
								self.total_cell_height)
						self.rects[c][r].append(rect)
				if not cell[self.SOUTH]:
					if c == num_cols - 1:
						rect = (c*self.total_cell_width,
								(r+1)*self.total_cell_height - wall_width,
								self.total_cell_width,
								wall_width)
						self.rects[c][r].append(rect)
					else:
						rect = (c*self.total_cell_width,
								(r+1)*self.total_cell_height-wall_width,
								self.total_cell_width+wall_width,
								wall_width)
						self.rects[c][r].append(rect)
				if not cell[self.WEST]:
					rect = (c*self.total_cell_width,
							r*self.total_cell_height,
							wall_width,
							self.total_cell_height) 
					self.rects[c][r].append(rect)
			
	def _discover( self, current_row , current_col ):
		self.cells[current_row][current_col][self.VISITED] = True
		
		directions = []
		for j in range(4):
			rand_dir = random.randint(self.NORTH,self.WEST)
			for i in range(4):
				dir = rand_dir - i
				if dir < 0:
					dir = 4 + dir
				if dir not in directions:
					directions.append(dir)
					break

		for direction in directions:
			if direction == self.NORTH and current_row > 0:
				if not self.cells[current_row-1][current_col][self.VISITED]:
					self.cells[current_row][current_col][self.NORTH] = True
					self.cells[current_row-1][current_col][self.SOUTH] = True
					try:
						self._discover(current_row-1,current_col)
					except RuntimeError as why:
						self.start_cells.append( (current_row-1,current_col) )
					continue
			elif direction == self.SOUTH and current_row < self.num_rows-1:
				if not self.cells[current_row+1][current_col][self.VISITED]:
					self.cells[current_row][current_col][self.SOUTH] = True
					self.cells[current_row+1][current_col][self.NORTH] = True
					try:
						self._discover(current_row+1,current_col)
					except RuntimeError as why:
						self.start_cells.append( (current_row+1,current_col) )
					continue
			elif direction == self.EAST and current_col < self.num_cols-1:
				if not self.cells[current_row][current_col+1][self.VISITED]:
					self.cells[current_row][current_col][self.EAST] = True
					self.cells[current_row][current_col+1][self.WEST] = True
					try:
						self._discover(current_row,current_col+1)
					except RuntimeError as why:
						self.start_cells.append( (current_row,current_col+1) )
					continue
			elif direction == self.WEST and current_col > 0:
				if not self.cells[current_row][current_col-1][self.VISITED]:
					self.cells[current_row][current_col][self.WEST] = True
					self.cells[current_row][current_col-1][self.EAST] = True
					try:
						self._discover(current_row,current_col-1)
					except RuntimeError as why:
						self.start_cells.append( (current_row,current_col-1) )
					continue

	def GetCellDimensions(self):
		return (self.num_cols, self.num_rows)

	def GetMazeRect(self):
		return self.maze_rect

	def Draw(self,surface,view_rect,wall_color=0xff0000):
		start_col,start_row,cell_width,cell_height = self.GetCellRange(view_rect)
		rects = self.rects
		for c in range(cell_width):
			col =  start_col+c
			for r in range(cell_height):
				row = start_row+r
				for wall in rects[col][row]:
					adjusted_wall = [ wall[0]-view_rect.left, wall[1]-view_rect.top, wall[2], wall[3] ]
					if adjusted_wall[0] < 0:
						adjusted_wall[2] = adjusted_wall[2] + adjusted_wall[0]
						adjusted_wall[0] = 0
					if adjusted_wall[1] < 0:
						adjusted_wall[3] = adjusted_wall[3] + adjusted_wall[1]
						adjusted_wall[1] = 0
					surface.fill(wall_color,adjusted_wall)

	def Collide(self,rect):
		retV = False
		cell_col = int(rect.left/self.total_cell_width)
		cell_row = int(rect.top/self.total_cell_height)
		
		for c in range(3):
			col = cell_col-1+c
			if col < 0 or col >= self.num_cols:
				continue
			for r in range(3):
				row = cell_row-1+r
				if row < 0 or row >= self.num_rows:
					continue
				for wall in self.rects[col][row]:
					if rect.colliderect(*wall):
						retV = True
						break
				if retV == True:
					break
			if retV == True:
				break
		return retV

	def GetCellRect(self,col,row):
		return pygame.Rect( col*self.total_cell_width+self.wall_width,
							row*self.total_cell_height+self.wall_width,
							self.cell_width,
							self.cell_height )

	def GetDeadEnds(self):
		retV = []
		for r in range(self.num_rows):
			for c in range(self.num_cols):
				if self.IsDeadEnd(c,r):
					retV.append( (c,r) )
		return retV

	def IsDeadEnd(self,col,row):
		cell = self.cells[row][col]
		if cell == [False,False,False,True,True] or \
		   cell == [False,False,True,False,True] or \
		   cell == [False,True,False,False,True] or \
		   cell == [True,False,False,False,True]:
			   return True
		else:
			return False

	def GetCellRange(self,rect):
		start_col = int(rect.left/self.total_cell_width)
		if start_col < 0:
			start_col = 0
		elif start_col >= self.num_cols:
			start_col = self.num_cols - 1
		
		width = int(rect.width/self.total_cell_width)
		if rect.width%self.total_cell_width:
			width = width + 1
		if rect.left%self.total_cell_width:
			width = width + 1
		if start_col+width >= self.num_cols:
			width = self.num_cols-start_col
		
		start_row = int(rect.top/self.total_cell_height)
		if start_row < 0:
			start_row = 0
		elif start_row >= self.num_rows:
			start_row = self.num_rows-1
			
		height = int(rect.height/self.total_cell_height)
		if rect.height%self.total_cell_height:
			height = height + 1
		if rect.top%self.total_cell_height:
			height = height + 1
		if start_row+height >= self.num_rows:
			height = self.num_rows-start_row

		return( start_col, start_row, width, height)

	def __str__( self ):
		string = " "
		for c in range(self.num_cols):
			cell = self.cells[0][c]
			if not cell[self.NORTH]:
				if c == self.num_cols - 1:
					string = string + "_"
				else:
					string = string + "__"
			else:
				string = string + "  "
		string = string + "\n"
		for r in range(self.num_rows):
			for c in range(self.num_cols):
				cell = self.cells[r][c]
				if not cell[self.WEST]:
					string = string + "|"
				else:
					string = string + "_"
					
				if not cell[self.SOUTH]:
					string = string + "_"
				else:
					string = string + " "
				
				if c == self.num_cols - 1:
					if not cell[self.EAST]:
						string = string + "|"
			string = string + "\n"
		return string

def _default_level_info(level_num):
	shaggy_speed = 5 + int(level_num/20)
	ghost_speed =  2 + ( 2 * int(level_num/20) )
	scooby_speed = 0 - int(level_num/30)

	maze_width = int(7 + (level_num-1)/10)
	maze_height = int(4 + (level_num-1)/5)
	
	num_ghosts = int((level_num+1)/2)

	return (maze_width, maze_height, num_ghosts,
			shaggy_speed, ghost_speed, scooby_speed)

class MouseTarget:
	def __init__(self,view_rect):
		self.view_rect = view_rect
	def GetPosition(self):
		view_rect = self.view_rect
		x_mpos, y_mpos = pygame.mouse.get_pos()
		return x_mpos+view_rect.left, y_mpos+view_rect.top
	def SetPosition(self,pos):
		x_pos,y_pos = pos
		view_rect = self.view_rect
		pygame.mouse.set_pos((x_pos-view_rect.left,y_pos-view_rect.top))

class Game:
	OPENING_PLAY = 0
	OPENING      = 1
	LOADING      = 3
	PLAYING_PLAY = 4
	PLAYING      = 5
	LOSER_PLAY   = 6
	LOSER        = 7
	WINNER_PLAY  = 8
	WINNER       = 9
	QUIT         = 10
	def __init__(self,level_info=_default_level_info,start_level=1):
		#General pygame intialization
		pygame.init()
		self.clock = pygame.time.Clock()
		try:
			self.joystick = pygame.joystick.Joystick(0)
		except pygame.error as msg:
			print("Could not find joystick")
			self.joystick = None
		else:
			self.joystick.init()
		self.bUseMouse = True
		self.mouse_target = None
		
		#Initalize background image and view port
		self.background = load_image("background.bmp",False)
		self.screen	 = pygame.display.set_mode(self.background.get_size())
		self.background.convert()
		self.view_rect  = pygame.Rect(0,0,0,0)
		self.panx_inc = 0
		self.pany_inc = 0
		self.view_rect.size = self.background.get_size()

		#Initialize the maze and the objects that go in it
		self.shaggy	  = MazeObject("shaggy")
		self.bang		= MazeObject("bang")
		self.demo_ghost  = MazeObject("ghost")
		self.demo_scooby = MazeObject("scooby")
		self.demo_door   = MazeObject("door")
		self.target_door = MazeObject("target_door")
		self.target_ghosts = []

		max_width  = 0
		max_height = 0
		for obj in [self.shaggy,self.demo_ghost,self.demo_scooby,self.demo_door]:
			width, height = obj.GetMaxSize()
			if width > max_width:
				max_width = width
			if height > max_height:
				max_height = height
		self.max_sprite_width  = max_width
		self.max_sprite_height = max_height

		self.shaggygroup = pygame.sprite.RenderPlain()
		self.banggroup   = pygame.sprite.RenderPlain()
		self.banggroup.add(self.bang)
		self.scoobygroup = pygame.sprite.RenderPlain()
		self.doorgroup   = pygame.sprite.RenderPlain()
		self.ghostgroup  = pygame.sprite.RenderPlain()

		self.door_pool = []
		self.door_locations = []

		self.maze = None
		self.shaggy_speed = 1
		self.shaggy_start = (0,0)
		self.ghost_speed  = 1
		self.scooby_speed = 0
		self.shaggy_hidden = 0
		self.dead_ghost = 0
		self.level = start_level
		self.level_info = level_info
		self.bConsolidateGhosts = False

		self.quick_attack_rect = pygame.Rect(0,0,0,0)
		self.quick_attack_rect.width = self.view_rect.width*2
		self.quick_attack_rect.height = self.view_rect.height*2
		
		#load sounds
		self.sounds = {}
		self.load_sound("opening")
		self.load_sound("loser")
		self.load_sound("winner")
		self.load_sound("door")
		self.load_sound("enter")
		self.load_sound("dead_ghost")

		#load pause screens
		self.opening_img = load_image("opening.bmp")
		self.loading_img = load_image("loading.bmp")
		self.winner_img = load_image("winner.bmp")
		self.loser_img = load_image("loser.bmp")

		#Create Font
		self.font = pygame.font.Font(os.path.join("data","game_font.ttf"),35)
		self.legal_font = pygame.font.Font(os.path.join("data","game_font.ttf"),10)

		#Create Cursors
		tmp = pygame.cursors.compile(up_cursor_strings,'.','X')
		self.up_cursor = (up_cursor_size,up_cursor_hotspot,tmp[0],tmp[1])
		tmp = pygame.cursors.compile(down_cursor_strings,'.','X')
		self.down_cursor = (down_cursor_size,down_cursor_hotspot,tmp[0],tmp[1])
		tmp = pygame.cursors.compile(left_cursor_strings,'.','X')
		self.left_cursor = (left_cursor_size,left_cursor_hotspot,tmp[0],tmp[1])
		tmp = pygame.cursors.compile(right_cursor_strings,'.','X')
		self.right_cursor = (right_cursor_size,right_cursor_hotspot,tmp[0],tmp[1])
		tmp = pygame.cursors.compile(center_cursor_strings,'.','X')
		self.center_cursor = (center_cursor_size,center_cursor_hotspot,tmp[0],tmp[1])
		pygame.mouse.set_cursor(*self.center_cursor)

	def load_sound(self,sound_name):
		full_name = os.path.join("data",sound_name)
		self.sounds[sound_name] = []
		count = 0
		while True:
			try:
				self.sounds[sound_name].append(pygame.mixer.Sound(full_name+str(count)+".wav"))
			except FileNotFoundError:
				break
			else:
				count = count + 1

	def play_sound(self,sound_name):
		if len(self.sounds[sound_name]) != 0:
			index = random.randint(0,len(self.sounds[sound_name])-1)
			self.sounds[sound_name][index].play()

	def stop_sound(self):
		sounds = self.sounds
		for key in sounds.keys():
			for sound in sounds[key]:
				sound.stop()

	def _GenerateLevel(self):
		maze_width, maze_height, num_ghosts, shaggy_speed, ghost_speed, scooby_speed = self.level_info(self.level)
		self.shaggy_speed = shaggy_speed
		self.ghost_speed = ghost_speed
		self.scooby_speed = scooby_speed
		self.maze = Maze(maze_width,maze_height,
							self.max_sprite_width+(2*self.shaggy_speed),
							self.max_sprite_height+(2*self.shaggy_speed),10)
		
		self._GenerateDoors()
		
		self._GenerateShaggy()
		self.shaggygroup.empty()
		self.shaggygroup.add(self.shaggy)

		self._GenerateScooby()
		self.scoobygroup.empty()
		self.scoobygroup.add(self.scooby)
	  
		self._GenerateGhosts(num_ghosts)
		self.ghostgroup.empty()
		self.ghostgroup.add(self.ghosts)

		self.view_rect.center = self.shaggy.GetMazeRect().center
		self.panx_inc = 0
		self.pany_inc = 0

		self.mouse_target = MouseTarget(self.view_rect)		

	def _GenerateShaggy(self):
		index = random.randint(0,len(self.door_locations)-1)
		self.shaggy_start = self.door_locations[index]
		self.shaggy.CenterOn(self.maze.GetCellRect(*self.shaggy_start))
		
		self.shaggy_hidden = time.time()+1
		
	def _GenerateScooby(self):
		num_cols, num_rows = self.maze.GetCellDimensions()
		while True:
			row = random.randint(0,num_rows-1)
			col = random.randint(0,num_cols-1)
			if (col,row) in self.door_locations or \
				abs(self.shaggy_start[0]-col) < int(num_cols/4) or \
				abs(self.shaggy_start[1]-row) < int(num_rows/4):
					continue
			else:
				self.scooby = MazeObject(demo=self.demo_scooby)
				self.scooby.CenterOn(self.maze.GetCellRect(col,row))
				break

	def _GenerateDoors(self):
		self.door_locations = self.maze.GetDeadEnds()
		self.door_pool = []
		rect = pygame.Rect(0,0,self.view_rect.width,self.view_rect.height)
		c,r,width,height = self.maze.GetCellRange(rect)
		for x in range((width+1)*(height+1)):
			self.door_pool.append(MazeObject(demo=self.demo_door))

	def _RefreshDoorGroup(self):
		cell_col, cell_row, cell_width, cell_height = self.maze.GetCellRange(self.view_rect)
		maze = self.maze
		self.doorgroup.empty() 
		index = 0
		for c in range(cell_width):
			col = cell_col + c
			for r in range(cell_height):
				row = cell_row + r
				if maze.IsDeadEnd(col,row):
					target_rect = maze.GetCellRect(col,row)
					if self.shaggy_hidden and target_rect.colliderect(self.shaggy.GetMazeRect()):
						self.target_door.CenterOn(target_rect)
						self.doorgroup.add(self.target_door)
					else:
						self.door_pool[index].CenterOn(target_rect)
						self.doorgroup.add(self.door_pool[index])
						index = index + 1

	def _GenerateGhosts(self,num_ghosts):
		self.ghosts = []
		ghosts = self.ghosts
		ghost_cells = []
		num_cols, num_rows = self.maze.GetCellDimensions()
		available_cells = (num_cols*num_rows)-len(self.door_locations)
		for i in range(num_ghosts):
			if len(ghost_cells) >= available_cells:
				break
			while True:
				row = random.randint(0,num_rows-1)
				col = random.randint(0,num_cols-1)
				if (col,row) in self.door_locations or \
						(col,row) in ghost_cells:
					continue
				else:
					cell_rect = self.maze.GetCellRect(col,row)
					new_ghost = MazeObject(demo=self.demo_ghost)
					new_ghost.CenterOn(cell_rect)
					ghosts.append(new_ghost)
					ghost_cells.append( (col,row) )
					break

	def _ConsolidateGhosts(self):
		i = 0
		j = 0
		ghosts = self.ghosts
		while i < len(ghosts):
			j = i + 1
			while j < len(ghosts):
				if ghosts[i].GetMazeRect().center == ghosts[j].GetMazeRect().center:
					self.ghostgroup.remove(ghosts[j])
					del ghosts[j]
				else:
					j = j + 1
			i = i + 1

	def _RunFrame(self):
		retV = self.PLAYING
		bUseDoor = False
		for event in pygame.event.get():
			if event.type == QUIT:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_SPACE:
				bUseDoor = True
			elif event.type == JOYBUTTONDOWN:
				bUseDoor = True
			elif event.type == KEYDOWN and event.key == K_m:
				if self.bUseMouse:
					self.bUseMouse = False
					pygame.mouse.set_cursor(*self.center_cursor)
				else:
					self.bUseMouse = True
					self.mouse_target.SetPosition(self.shaggy.GetMazeRect().center)
			elif self.bUseMouse and event.type == MOUSEBUTTONDOWN:
				bUseDoor = True
		
		#Handle Shaggy's movement
		x_offset = 0
		y_offset = 0
		if self.bUseMouse:
			if not self.shaggy_hidden:
				self.shaggy.Attack(self.maze,self.mouse_target,self.shaggy_speed)
				if self.mouse_target.GetPosition() == self.shaggy.GetMazeRect().center:
					pygame.mouse.set_cursor(*self.center_cursor)
				else:
					dir = self.shaggy.GetDirection()
					if dir == self.shaggy.D_UP:
						pygame.mouse.set_cursor(*self.up_cursor)
					elif dir == self.shaggy.D_DOWN:
						pygame.mouse.set_cursor(*self.down_cursor)
					elif dir == self.shaggy.D_LEFT:
						pygame.mouse.set_cursor(*self.left_cursor)
					elif dir == self.shaggy.D_RIGHT:
						pygame.mouse.set_cursor(*self.right_cursor)
		else:
			if self.joystick != None:
				x_offset = int(round(self.shaggy_speed*self.joystick.get_axis(0)))
				y_offset = int(round(self.shaggy_speed*self.joystick.get_axis(1)))
			if x_offset == 0 and y_offset == 0:
				keys = pygame.key.get_pressed()
				if keys[K_UP]:
					y_offset = y_offset - self.shaggy_speed
				if keys[K_DOWN]:
					y_offset = y_offset + self.shaggy_speed
				if keys[K_RIGHT]:
					x_offset = x_offset + self.shaggy_speed
				if keys[K_LEFT]:
					x_offset = x_offset - self.shaggy_speed
			if not self.shaggy_hidden:
				self.shaggy.Move(self.maze,x_offset,y_offset)

		#Refresh the sprites and display considering the recent movement.
		shaggy_rect = self.shaggy.GetMazeRect()
		maze_rect   = self.maze.GetMazeRect()
		view_rect   = self.view_rect
		
		if view_rect.width >= maze_rect.width:
			view_rect.centerx = maze_rect.centerx
		else:
			if self.shaggy_hidden:
				if abs(self.panx_inc) > abs(view_rect.centerx-shaggy_rect.centerx):
					view_rect.centerx = shaggy_rect.centerx
				else:
					view_rect.centerx = view_rect.centerx + self.panx_inc
			else:
				view_rect.centerx = shaggy_rect.centerx
			if view_rect.left < maze_rect.left:
				view_rect.left = maze_rect.left
			elif view_rect.right > maze_rect.right:
				view_rect.right = maze_rect.right
		if view_rect.height >= maze_rect.height:
			view_rect.centery = maze_rect.centery
		else:
			if self.shaggy_hidden:
				if abs(self.pany_inc) > abs(view_rect.centery-shaggy_rect.centery):
					view_rect.centery = shaggy_rect.centery
				else:
					view_rect.centery = view_rect.centery  + self.pany_inc
			else:
				view_rect.centery = shaggy_rect.centery
			if view_rect.top < maze_rect.top:
				view_rect.top = maze_rect.top
			elif view_rect.bottom > maze_rect.bottom:
				view_rect.bottom = maze_rect.bottom

		#Let the ghost give chase
		ghost_speed = self.ghost_speed
		if self.shaggy_hidden:
			ghost_speed = 0-ghost_speed
		quick_attack = False
		if self.clock.get_time() > 1000.0/float(FRAMES_PER_SECOND):
			quick_attack = True
			self.quick_attack_rect.left = view_rect.left-view_rect.width
			self.quick_attack_rect.top  = view_rect.top-view_rect.height

		for ghost in self.ghosts:
			if ghost not in self.target_ghosts:
				if quick_attack:
					if ghost.GetMazeRect().colliderect(self.quick_attack_rect):
						ghost.Attack(self.maze,self.shaggy,ghost_speed)
				else:
					ghost.Attack(self.maze,self.shaggy,ghost_speed)
			else:
				ghost.Attack(self.maze,self.shaggy,self.ghost_speed)
		self.scooby.Attack(self.maze,self.shaggy,self.scooby_speed)

		self._RefreshDoorGroup()
		self.doorgroup.update(view_rect)
		self.ghostgroup.update(view_rect)
		self.scoobygroup.update(view_rect)
		self.shaggygroup.update(view_rect)
		self.banggroup.update(view_rect)

		self.screen.blit(self.background,(0,0))
		self.maze.Draw(self.screen,view_rect)
		self.doorgroup.draw(self.screen)
		self.ghostgroup.draw(self.screen)
		self.scoobygroup.draw(self.screen)
		if not self.shaggy_hidden:
			self.shaggygroup.draw(self.screen)
		if self.dead_ghost:
			self.banggroup.draw(self.screen)
		pygame.display.flip()

		if self.dead_ghost:
			if self.bUseMouse:
				self.mouse_target.SetPosition(self.shaggy.GetMazeRect().center)
				pygame.mouse.set_cursor(*self.center_cursor)
			if self.bConsolidateGhosts:
				self._ConsolidateGhosts()
				self.bConsolidateGhosts = False
			if time.time() >= self.dead_ghost:
				self.dead_ghost = 0
				self.shaggy_hidden = 0
				self.target_ghosts = []
		elif self.shaggy_hidden:
			if self.bUseMouse:
				self.mouse_target.SetPosition(self.shaggy.GetMazeRect().center)
				pygame.mouse.set_cursor(*self.center_cursor)
			if time.time() >= self.shaggy_hidden:
				self.shaggy_hidden = 0
				self.panx_inc = 0
				self.pany_inc = 0
				
				if len(self.target_ghosts) > 0:				
					self.play_sound("dead_ghost")
					self.dead_ghost = time.time()+1
					self.shaggy_hidden = 1
					self.bang.CenterOn(self.shaggy.GetMazeRect())
					for ghost in self.target_ghosts:
						self.ghostgroup.remove(ghost)
						del self.ghosts[self.ghosts.index(ghost)]
					self.bConsolidateGhosts = True
		else:
			#Check for relevant collisions
			if pygame.sprite.spritecollideany( self.shaggy, self.ghostgroup ) != None:
				retV = self.LOSER_PLAY
				pygame.mouse.set_cursor(*self.center_cursor)
			elif pygame.sprite.spritecollideany( self.shaggy, self.scoobygroup ) != None:
				retV = self.WINNER_PLAY
				pygame.mouse.set_cursor(*self.center_cursor)
			elif bUseDoor:
				door = pygame.sprite.spritecollideany( self.shaggy, self.doorgroup )
				if door != None:
					current_col,current_row,w,h = self.maze.GetCellRange(door.GetMazeRect())
					num_cols, num_rows = self.maze.GetCellDimensions()
					direction = self.shaggy.GetDirection()
					b_less_than_first = random.randint(0,1)
					target = None
					if direction == self.shaggy.D_UP or direction == self.shaggy.D_DOWN:
						if b_less_than_first:
							col_list = [current_col,current_col-1,current_col+1]
						else:
							col_list = [current_col,current_col+1,current_col-1]
						if direction == self.shaggy.D_UP:
							adder = -1
						else:
							adder = 1
						r = current_row + adder
						while True:
							if r < 0:
								r = num_rows
							elif r >= num_rows:
								r = -1
							else:
								for c in col_list:
									if c < 0 or c >= num_cols:
										continue
									elif c == current_col and r == current_row:
										continue
									else:
										if self.maze.IsDeadEnd(c,r):
											target = (c,r)
											break
							if target != None:
								break
							elif r == current_row:
								break
							else:
								r = r + adder
					else:
						if b_less_than_first:
							row_list = [current_row, current_row-1, current_row+1]
						else:
							row_list = [current_row, current_row+1, current_row-1]
						if direction == self.shaggy.D_LEFT:
							adder = -1
						else:
							adder = 1
						c = current_col + adder
						while True:
							if c < 0:
								c = num_cols
							elif c >= num_cols:
								c = -1
							else:
								for r in row_list:
									if r < 0 or r >= num_rows:
										continue
									elif c == current_col and r == current_row:
										continue
									else:
										if self.maze.IsDeadEnd(c,r):
											target = (c,r)
											break
							if target != None:
								break
							elif c == current_col:
								break
							else:
								c = c + adder
					if target == None:
						while True:
							index = random.randint(0,len(self.door_locations)-1)
							c, r = self.door_locations[index]
							if c == current_col and r == current_row:
								continue
							else:
								target = (c,r)
								break		  
					target_maze_rect = self.maze.GetCellRect(*target)
					self.shaggy.CenterOn(target_maze_rect)
					self.play_sound("door")
					self.shaggy_hidden = time.time()+1

					for ghost in self.ghosts:
						if target_maze_rect.colliderect(ghost.GetMazeRect()):
							self.target_ghosts.append(ghost)

					pan_step = int(self.clock.get_fps()/2)
					
					self.panx_inc = self.shaggy.GetMazeRect().centerx-self.view_rect.centerx
					if self.panx_inc > 0-pan_step and self.panx_inc < 0:
						self.panx_inc = -1
					elif self.panx_inc < pan_step and self.panx_inc > 0:
						self.panx_inc = 1
					else:
						self.panx_inc = int(self.panx_inc/pan_step)
					self.pany_inc = self.shaggy.GetMazeRect().centery-self.view_rect.centery
					if self.pany_inc > 0-pan_step and self.pany_inc < 0:
						self.pany_inc= -1
					elif self.pany_inc < pan_step and self.pany_inc > 0:
						self.pany_inc = 1
					else:
						self.pany_inc =  int(self.pany_inc/pan_step)
		return retV

	def _ShowOpening(self):
		retV = self.OPENING
		for event in pygame.event.get():
			if event.type == QUIT:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_SPACE:
				retV = self.LOADING
			elif event.type == JOYBUTTONDOWN:
				retV = self.LOADING
			elif self.bUseMouse and event.type == MOUSEBUTTONDOWN:
				retV = self.LOADING
			elif event.type == KEYDOWN and event.key == K_m:
				if self.bUseMouse:
					self.bUseMouse = False
				else:
					self.bUseMouse = True
				
		view_width, view_height = self.screen.get_size()
		opening_width, opening_height = self.opening_img.get_size()
		self.screen.blit(self.background,(0,0))
		self.screen.blit(self.opening_img,( int((view_width-opening_width)/2), int((view_height-opening_height)/2) ))

		copyright_text = self.legal_font.render("Game Engine Copyright (c) 2005 Dan Tabor. All rights reserved.",1,pygame.color.Color('0xff0000'))
		img_width, img_height = copyright_text.get_size()
		self.screen.blit(copyright_text,(view_width-img_width,view_height-(2*img_height)))

		disclaimer_text = self.legal_font.render("All images and sound are owned by their respective copyright holders.",1,pygame.color.Color('0xff0000'))
		img_width, img_height = disclaimer_text.get_size()
		self.screen.blit(disclaimer_text,(view_width-img_width,view_height-img_height))

		text = self.font.render("Press button to enter level %d" % int(self.level),1,pygame.color.Color('0xff0000'))
		img_width, img_height = text.get_size()
		self.screen.blit(text,( int((view_width-img_width)/2), int(view_height-(1.5*img_height)) ))
		
		pygame.display.flip()
		return retV

	def _ShowWinner(self):
		retV = self.WINNER
		for event in pygame.event.get():
			if event.type == QUIT:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_SPACE:
				retV = self.LOADING
			elif event.type == JOYBUTTONDOWN:
				retV = self.LOADING
			elif self.bUseMouse and event.type == MOUSEBUTTONDOWN:
				retV = self.LOADING
			elif event.type == KEYDOWN and event.key == K_m:
				if self.bUseMouse:
					self.bUseMouse = False
				else:
					self.bUseMouse = True
				
		view_width, view_height = self.screen.get_size()
		img_width, img_height = self.winner_img.get_size()
		self.screen.blit(self.background,(0,0))
		self.screen.blit(self.winner_img,( int((view_width-img_width)/2), int((view_height-img_height)/2) ))

		text = self.font.render("Press button to enter level %d" % int(self.level),1,pygame.color.Color('0xff0000'))
		img_width, img_height = text.get_size()
		self.screen.blit(text,(int((view_width-img_width)/2),int(view_height-(1.5*img_height)) ))

		pygame.display.flip()
		return retV

	def _ShowLoading(self):
		retV = self.LOADING
		for event in pygame.event.get():
			if event.type == QUIT:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_m:
				if self.bUseMouse:
					self.bUseMouse = False
				else:
					self.bUseMouse = True
				
		view_width, view_height = self.screen.get_size()
		img_width, img_height = self.loading_img.get_size()
		self.screen.blit(self.background,(0,0))
		self.screen.blit(self.loading_img,( int((view_width-img_width)/2), int((view_height-img_height)/2) ))

		text = self.font.render("Loading level %d..." % int(self.level),1,pygame.color.Color('0xff0000'))
		img_width, img_height = text.get_size()
		self.screen.blit(text,(int((view_width-img_width)/2),int(view_height-(1.5*img_height)) ))

		pygame.display.flip()
		return retV

	def _ShowLoser(self):
		retV = self.LOSER
		for event in pygame.event.get():
			if event.type == QUIT:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				retV = self.QUIT
			elif event.type == KEYDOWN and event.key == K_SPACE:
				retV = self.LOADING
			elif event.type == JOYBUTTONDOWN:
				retV = self.LOADING
			elif self.bUseMouse and event.type == MOUSEBUTTONDOWN:
				retV = self.LOADING
			elif event.type == KEYDOWN and event.key == K_m:
				if self.bUseMouse:
					self.bUseMouse = False
				else:
					self.bUseMouse = True
				
		view_width, view_height = self.screen.get_size()
		img_width, img_height = self.loser_img.get_size()
		self.screen.blit(self.background,(0,0))
		self.screen.blit(self.loser_img,( int((view_width-img_width)/2), int((view_height-img_height)/2) ))

		text = self.font.render("Press button to retry level %d" % int(self.level),1,pygame.color.Color('0xff0000'))
		img_width, img_height = text.get_size()
		self.screen.blit(text,(int((view_width-img_width)/2), int(view_height-(1.5*img_height)) ))	  
		
		pygame.display.flip()
		return retV

	def Run(self):
		load_thread = None
		state = self.OPENING_PLAY
		
		while 1:
			self.clock.tick(int(FRAMES_PER_SECOND))
			if state == self.OPENING_PLAY:
				self.play_sound("opening")
				state = self._ShowOpening()
			elif state == self.OPENING:
				state = self._ShowOpening()
			elif state == self.LOADING:
				if load_thread == None:
					load_thread = threading.Thread(None,self._GenerateLevel,"GenerateLevel")
					load_thread.start()
				state = self._ShowLoading()
			elif state == self.PLAYING_PLAY:
				self.stop_sound()
				self.play_sound("enter")
				state = self._RunFrame()
			elif state == self.PLAYING:
				state = self._RunFrame()
			elif state == self.LOSER_PLAY:
				self.stop_sound()
				self.play_sound("loser")
				state = self._ShowLoser()
			elif state == self.LOSER:
				state = self._ShowLoser()
			elif state == self.WINNER_PLAY:
				self.level = self.level+1
				self.stop_sound()
				self.play_sound("winner")
				state = self._ShowWinner()
			elif state == self.WINNER:
				state = self._ShowWinner()
			else:
				break
			   
			if load_thread != None:
				if not load_thread.is_alive():
					load_thread = None
					state = self.PLAYING_PLAY
			
def parent_level_info(level_num):
	shaggy_speed = 10
	ghost_speed =  int(shaggy_speed * 0.75)
	scooby_speed = 0 - shaggy_speed

	maze_width = int(6 + level_num/2)
	maze_height = int(4 + level_num/4)
	
	num_ghosts = maze_width*maze_height

	return (maze_width, maze_height, num_ghosts,
			shaggy_speed, ghost_speed, scooby_speed)

def guantlet_level_info(level_num):
	return 100*level_num,100*level_num,1000*level_num,10,8,-5

def usage():
	print("Usage:")
	print("   scooby_maze.py [-h] [-p or -g] [-l level] [-y]")
	print("")
	print("h - Show this message")
	print("p - Parent Mode (much harder)")
	print("g - Gauntlet Mode (impossible)")
	print("l - Start at specified level")
	sys.exit(1)
	
if __name__=="__main__":
	level_info = None
	start_level = 1
	i = 1
	if len(sys.argv) > 1:
		while i < len( sys.argv ):
			if sys.argv[i] == "-h":
				usage()
			elif sys.argv[i] == "-p":
				level_info = parent_level_info
			elif sys.argv[i] == "-g":
				level_info = guantlet_level_info
			elif sys.argv[i] == "-l" and len(sys.argv) > i+1:
				try:
					start_level = int(sys.argv[i+1])
				except Exception:
					usage()
				else:
					i = i + 1
			else:
				usage()
			i = i + 1
	if level_info != None:
		obj = Game(level_info,start_level=start_level)
	else:
		obj = Game(start_level=start_level)
	obj.Run()