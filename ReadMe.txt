Scooby Doo and the Haunted Maze
=======================================================================

For children who grow up watching their parents use computers, it is 
natural for them to want to take part in using computer system.  
Unfortunately, there is a shortage of computer programs that children 
~4-5 can attempt to use in any meaningful manner and not become easily 
frustrated.  This game was original created to help fill that void for 
a very special child in my life.

If you are planning on modifying this game or redistributing it, please 
read the LICENSE file and the developers section below.


Game Play:
==========
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

Any on screen instructions that refer to pressing a button are 
referring to any joystick button, or the space bar.

Update for version 1.1:  The game now supports mouse input.  The 
"action button" is any mouse button.  When mouse input is turned on
Shaggy will attempt to move toward the mouse cursor.  The cursor will
change depending upon how Shaggy moves to try to reach it.  When mouse
input is turned on, joystick and keyboard input is disabled.  Mouse
input is on by default, but can be toggled by pressing the 'm' key.


Command Line Options:
=====================
Whether you are  using a .py file or a .exe windows executable, their 
are command line arguments available to you.  Here is the usage 
statement:

	    Usage:
              scooby_maze.py [-h] [-p or -g] [-l level] [-y]
          
           h - Show this message
           p - Parent Mode (much harder)
           g - Gauntlet Mode (impossible)
           l - Start at specified level
           y - Attempt to use psyco to improve performance
                  (generally not recommended)

Parent mode is incase parents find themselves bored and want to play 
"that Scooby Doo game", but don't want it to bore them even more.

Gauntlet mode exists mostly for doing optimization testing.  It pushes 
the limits of what the game can handle (Python was not designed for 
doing massive game development).  This mode also pushes the limits of 
how big a maze can be and still be considered remotely entertaining.

If a start level is given it will be applied to whatever mode the game 
is in.

For people unfamiliar with psyco it can be used to speed up execution 
of Python programs on x86 machines by doing memory and assembly level 
code analysis and replacement.  Sort of like having a JIT compiler that 
actually runs inline with the code it’s compiling.  This is a terrific 
technology that allows normal Python code to have a higher average 
execution speed.  However, psyco does not yield consistent execution 
times, and the game engine employs optimization techniques that work 
best when execution time is fairly consistent.  Use of psyco is not 
recommended unless your experiencing game speed problems in level 1 of 
the normal mode.  


Developers:
===========
This game was originally developed with a Scooby Doo theme.  This 
caused the game engine to be released under a separate license than the 
images and sounds due to legal reasons that I will not attempt to 
understand, but know exist.  The game engine is designed to be flexible 
based on the files found in the 'data' directory. (For example the 
window size is the same as the size of the background image and the 
maze hallway widths are determined by the shaggy, ghost, door, and 
scooby image sets).  The naming convention should be fairly easy to 
follow to someone who has played game.  So changing this theme to 
something more suitable for your own situation can be done with exactly 
zero code editing.

If you should also like to modify the game play, the game engine is 
written in Python and utilizes pygame (a libsdl extension and wrapper).  
Comments are sparse, but I wish you good luck.  In addition, I’ve very 
curious about people who might use my work, so I’d appreciate an e-mail 
letting me know what you’re doing and perhaps code patches if you 
choose to keep the same license for your code.
