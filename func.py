import pygame, sys, random
from pygame.locals import *
import glob
from pygame import mixer
from mutagen.mp3 import MP3

# Tạo sẵn các màu sắc
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
SILVER = (215, 215, 215)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE = (255, 140, 0)
EMPTY = (0, 0, 0, 0)
# Thông số cơ bản của màn hình hiển thị
WINDOWWIDTH = 400
WINDOWHEIGHT = 600

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), SRCALPHA, pygame.RESIZABLE)
programIcon = pygame.image.load('image/edit.png')
programIcon = pygame.transform.scale(programIcon, (15, 15))
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Music Application')
