#setup.py
from distutils.core import setup
import pygame
import os

try:
    import py2exe
except ImportError:
    print "py2exe is unavailable"
try:
    import py2app
except ImportError:
    print "py2app is unavailable"


data_files = []
for file in os.listdir("data"):
    data_files.append("/".join(("data",file)))

#pygamedir = os.path.split(pygame.base.__file__)[0]
#pygame_files = [os.path.join(pygamedir, pygame.font.get_default_font())]

setup(name="ScoobyMaze",
      version = "1.1",
      description="Scooby Doo and the Haunted Maze",
      author="Dan Tabor",
      author_email="daniel.tabor@gmail.com",
      windows=[{
                  "script":"scooby_maze.py",
                  "icon_resources":[(1,"scooby_maze.ico")]
                }],
      data_files=[(".",
                   ["ReadMe.txt","LICENSE"]),
                  ("data",
                   data_files)],
      app = ['scooby_maze.py'],
      options={"py2app":{"iconfile":"scooby_maze.icns"}},
      )
