import pygame
import sys
import minesweeper as msw
from math import floor

# pygame SETTINGS

screenSize = [1080, 720]


print("Map size: example \"25, 25\"\n")
sizeinp = input()
if sizeinp:
    sizeinp = sizeinp.split(",")
else:
    sizeinp = (25, 25)

print("Bomb amount \n")
amountinp = input()
if amountinp == "":
    amountinp=50

# MINESWEEPER SETTINGS
MAPSIZE = [int(sizeinp[0]), int(sizeinp[1])]
BOMBAMOUNT = int(amountinp)
bomblist = msw.createbomblist(MAPSIZE, BOMBAMOUNT)
map = msw.createmap(MAPSIZE, bomblist)
renderMap = [[None for _ in range(MAPSIZE[0])] for _ in range(MAPSIZE[1])]


# button sizes
BUTTONSIZE = None
xsize = int(screenSize[0]/MAPSIZE[0])
ysize = int(screenSize[1]/MAPSIZE[1])

offset = [0, 0]
if xsize < ysize:
    BUTTONSIZE = xsize
else:
    BUTTONSIZE = ysize

offset[0] = (screenSize[0] - MAPSIZE[0]*BUTTONSIZE)/2
offset[1] = (screenSize[1] - MAPSIZE[1]*BUTTONSIZE)/2




# initializing pygame
pygame.init()
display = pygame.display.set_mode((screenSize[0], screenSize[1]))

def show3x3tiles(pos):
    global renderMap
    if pos[1] != 0:
        if pos[0] != 0:
            renderMap[pos[0]-1][pos[1]-1] = map[pos[0]-1][pos[1]-1]

        renderMap[pos[0]+0][pos[1]-1] = map[pos[0]+0][pos[1]-1]

        if pos[0] != len(map[0])-1:
            renderMap[pos[0]+1][pos[1]-1] = map[pos[0]+1][pos[1]-1]

    if pos[0] != 0:
        renderMap[pos[0]-1][pos[1]] = map[pos[0]-1][pos[1]]

    renderMap[pos[0]][pos[1]] = map[pos[0]][pos[1]]

    if pos[0] != len(map[0])-1:
        renderMap[pos[0]+1][pos[1]] = map[pos[0]+1][pos[1]]

    if pos[1] != len(map[1])-1:
        if pos[0] != 0:
            renderMap[pos[0]-1][pos[1]+1] = map[pos[0]-1][pos[1]+1]

        renderMap[pos[0]+0][pos[1]+1] = map[pos[0]+0][pos[1]+1]

        if pos[0] != len(map[0])-1:
            renderMap[pos[0]+1][pos[1]+1] = map[pos[0]+1][pos[1]+1]

def emptytile(pos):
    global renderMap
    emptytileslist = [pos]
    alreadyhad = [pos]

    while len(emptytileslist) != 0:
        ipos = emptytileslist.pop()
        show3x3tiles(ipos)
        for i in msw.checkempty(map, ipos):
            if i not in alreadyhad:
                emptytileslist.append(i)
                alreadyhad.append(i)




# loading imgs
loadlist = ["button", "one", "two", "three", "four", "five", "six", "seven", "eight", "bomb", "flag"]
loadedlist = {}
for name in loadlist:
    loadedlist[name] = pygame.image.load(f"{name}.png").convert()
    loadedlist[name] = pygame.transform.scale(loadedlist[name], (BUTTONSIZE, BUTTONSIZE))

WINIMG = pygame.image.load(f"win.png").convert()
WINIMG = pygame.transform.scale(WINIMG, (int(screenSize[0]/2), int(screenSize[1]/2)))

LOSSIMG = pygame.image.load(f"boom.png").convert()
LOSSIMG = pygame.transform.scale(LOSSIMG, (int(screenSize[0]/2), int(screenSize[1]/2)))





leftmousepressed = 0
rightmousepressed = 0
rpressed = 0

win = None
paused = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # actions
    if not paused:

        if pygame.mouse.get_pressed() == (0, 0, 0):
            leftmousepressed = 0
            rightmousepressed = 0
        # LEFT MOUSE
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if leftmousepressed == 0:
                leftmousepressed = 1
                mousepos = pygame.mouse.get_pos()
                x = floor((mousepos[0]-offset[0])/BUTTONSIZE)
                y = floor((mousepos[1]-offset[1])/BUTTONSIZE)

                if not (x < 0 or x > MAPSIZE[0]-1):
                    if not (y < 0 or y > MAPSIZE[1]-1):
                        if renderMap[x][y] == None:
                            renderMap[x][y] = map[x][y]
                            if renderMap[x][y] == 0:
                                emptytile((x,y))
                            if renderMap[x][y] == "B":
                                for bpos in bomblist:
                                    renderMap[bpos[0]][bpos[1]] = map[bpos[0]][bpos[1]]
                                paused = True
                                win = False
        # RIGHT MOUSE
        if pygame.mouse.get_pressed() == (0, 0, 1):
            if rightmousepressed == 0:
                rightmousepressed = 1
                mousepos = pygame.mouse.get_pos()
                x = floor((mousepos[0]-offset[0])/BUTTONSIZE)
                y = floor((mousepos[1]-offset[1])/BUTTONSIZE)

                if not (x < 0 or x > MAPSIZE[0]-1):
                    if not (y < 0 or y > MAPSIZE[1]-1):
                        if renderMap[x][y] == None:
                            renderMap[x][y] = "F"
                        elif renderMap[x][y] == "F":
                            renderMap[x][y] = None

        # COUNT
        amount = 0
        for y in range(MAPSIZE[1]):
            for x in range(MAPSIZE[0]):
                if renderMap[x][y] == None or renderMap[x][y] == "F":
                    amount+=1
        if amount == BOMBAMOUNT:
            paused = True
            print("YOU WON!")
            win = True
            for bpos in bomblist:
                renderMap[bpos[0]][bpos[1]] = "F"

    keys=pygame.key.get_pressed()
    if keys[pygame.K_r]:
        if rpressed == 0:
            rpressed = 1

            bomblist = msw.createbomblist(MAPSIZE, BOMBAMOUNT)
            map = msw.createmap(MAPSIZE, bomblist)
            renderMap = [[None for _ in range(MAPSIZE[0])] for _ in range(MAPSIZE[1])]
            win = None
            paused = False
    else:
        rpressed = 0


    # clear screen
    display.fill((200, 200, 220))
    # draw scrren


    for y in range(MAPSIZE[1]):
        for x in range(MAPSIZE[0]): # TODO: PLS FIX
            if renderMap[x][y] == None:
                display.blit(loadedlist["button"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 1:
                display.blit(loadedlist["one"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 2:
                display.blit(loadedlist["two"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 3:
                display.blit(loadedlist["three"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 4:
                display.blit(loadedlist["four"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 5:
                display.blit(loadedlist["five"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 6:
                display.blit(loadedlist["six"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 7:
                display.blit(loadedlist["seven"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == 8:
                display.blit(loadedlist["eight"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == "F":
                display.blit(loadedlist["flag"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))
            elif renderMap[x][y] == "B":
                display.blit(loadedlist["bomb"], (int(x*BUTTONSIZE+offset[0]), int(y*BUTTONSIZE+offset[1])))

    if win == True:
        display.blit(WINIMG, (int(screenSize[0]/4), int(screenSize[1]/4)))
    elif win == False:
        display.blit(LOSSIMG, (int(screenSize[0]/4), int(screenSize[1]/4)))

    # update screen
    pygame.display.flip()

pygame.quit()
