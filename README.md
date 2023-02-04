Scooby Doo and the Haunted Maze
=======================================================================
![scooby_maze_screenshot](https://user-images.githubusercontent.com/70762874/216735029-1c59d8e9-0926-41c6-ad77-dce3ca96980e.jpg)

I originally wrote this for my niece when she was 4.  It was originally
written for Python 2.X and had scripts for packaging up a Windows

installer and a Mac dmg.  I've updated it to work with Python 3 and 
modern pygame.

## Game Play ##
You play the role of Shaggy, who finds himself lost in a haunted maze 
separated from is good old pal, Scooby Doo.  You may either use a 
joystick or keyboard to move Shaggy around the maze, in order to find 
his wet noised friend, while trying to avoid the ghosts (a.k.a. guys in 
masks) that inevitably inhabit a haunted maze.  Finding Scooby will 
cause Shaggy to progress to the next level.  Finding a ghost will cause 
Shaggy to repeat the level.  Doors are provided to help you avoid and 
defeat your fiendish foes.  You will find a door at every dead end in 
the maze.  Simple hit the space bar (or a joystick button) when over a 
door and you will use an expansive (off screen) system of hallways and 
emerge at another door.  Doors are directional, so Shaggy will 
_attempt_ to emerge at a door in about the same direction as the one he 
was facing when he entered a door.  If a ghost is standing over a door 
when Shaggy emerges from it, the door will swing open, hitting the 
ghost and eliminating him from the game.  Mazes are completely randomly 
generated so even if you have to repeat a level it is fairly unlikely 
you will see the same one twice in a row.  Levels are defined by how 
large the mazes are, how many ghosts there are, etc., not the layout of 
the maze.

To quit the game, close the window or hit the ESC key.

When mouse input is turned on Shaggy will attempt to move toward the 
mouse cursor.  The cursor will change depending upon how Shaggy moves to 
try to reach it.  When mouse input is turned on, joystick and keyboard 
input is disabled.  Mouse input is on by default, but can be toggled by 
pressing the 'm' key.

Any on screen instructions that refer to pressing a button are 
referring to any joystick button, left mouse button, or the space bar.

## Usage ##
```
Usage:
   scooby_maze.py [-h] [-p] [-l level]

h - Show this message
p - Parent Mode (much harder)
l - Start at specified level
```
If a start level is given it will be applied to whatever mode the game 
is in.
