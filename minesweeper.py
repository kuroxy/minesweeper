import random


def createpos(mapSize):
    x = random.randrange(mapSize[0])
    y = random.randrange(mapSize[1])
    return (x,y)

def createbomblist(mapSize, bombAmount):
    if mapSize[0] * mapSize[1] <= bombAmount:
        print("couldnt create bomblist, bombamount too big")
        return False

    tempbomblist = []
    while len(tempbomblist) < bombAmount:
        newpos = createpos(mapSize)
        if not newpos in tempbomblist:
            tempbomblist.append(newpos)

    return tempbomblist


# [-1][-1] , [0][-1], [1][-1]
# [-1][0] , [0][0], [1][0]
# [-1][1] , [0][1], [1][1]

def checktile(map, pos):
    bombcount = 0

    if pos[1] != 0:
        if pos[0] != 0:
            if map[pos[0]-1][pos[1]-1] == "B":
                bombcount+=1

        if map[pos[0]+0][pos[1]-1] == "B":
            bombcount+=1

        if pos[0] != len(map[0])-1:
            if map[pos[0]+1][pos[1]-1] == "B":
                bombcount+=1

    if pos[0] != 0:
        if map[pos[0]-1][pos[1]] == "B":
            bombcount+=1

    if pos[0] != len(map[0])-1:
        if map[pos[0]+1][pos[1]] == "B":
            bombcount+=1

    if pos[1] != len(map[1])-1:
        if pos[0] != 0:
            if map[pos[0]-1][pos[1]+1] == "B":
                bombcount+=1

        if map[pos[0]+0][pos[1]+1] == "B":
            bombcount+=1

        if pos[0] != len(map[0])-1:
            if map[pos[0]+1][pos[1]+1] == "B":
                bombcount+=1

    return bombcount

def checkempty(map, pos):
    emptylist = []

    if pos[1] != 0:
        if pos[0] != 0:
            if map[pos[0]-1][pos[1]-1] == 0:
                emptylist.append((pos[0]-1,pos[1]-1))

        if map[pos[0]+0][pos[1]-1] == 0:
            emptylist.append((pos[0],pos[1]-1))

        if pos[0] != len(map[0])-1:
            if map[pos[0]+1][pos[1]-1] == 0:
                emptylist.append((pos[0]+1,pos[1]-1))

    if pos[0] != 0:
        if map[pos[0]-1][pos[1]] == 0:
            emptylist.append((pos[0]-1,pos[1]))

    if pos[0] != len(map[0])-1:
        if map[pos[0]+1][pos[1]] == 0:
            emptylist.append((pos[0]+1,pos[1]))

    if pos[1] != len(map[1])-1:
        if pos[0] != 0:
            if map[pos[0]-1][pos[1]+1] == 0:
                emptylist.append((pos[0]-1,pos[1]+1))

        if map[pos[0]+0][pos[1]+1] == 0:
            emptylist.append((pos[0],pos[1]+1))

        if pos[0] != len(map[0])-1:
            if map[pos[0]+1][pos[1]+1] == 0:
                emptylist.append((pos[0]+1,pos[1]+1))

    return emptylist



def createmap(mapSize, bomblist):
    tempMap = [[0 for _ in range(mapSize[0])] for _ in range(mapSize[1])]

    for bpos in bomblist:
        tempMap[bpos[0]][bpos[1]] = "B"

    for y in range(mapSize[1]):
        for x in range(mapSize[0]):
            if tempMap[x][y] == "B" :
                continue
            tempMap[x][y] = checktile(tempMap, (x, y))
    return tempMap


if __name__ == "__main__":
    MapSize = (25, 25)
    BombAmount = 50

    map = createmap(MapSize, createbomblist(MapSize, BombAmount))
    for i in map:
        print(i)
