#!/usr/bin/python
import random
from collections import deque

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        coorStr = "[" + str(self.x) + "," + str(self.y) + "]"
        return coorStr

class Board():
    def __init__(self):
        self.matrix = [([0] * 4) for pos in xrange(4)]

    def __str__(self):
        """
        For printing the board:
        """
        output = ""
        for posVert in self.matrix:
            output += "_____________________________\n"
            for posHor in posVert:
                output += " | "
                if posHor < 10:
                    output += " " + str(posHor) + "  "
                elif posHor < 100:
                    output += " " + str(posHor) + " "
                elif posHor < 1000:
                    output += str(posHor) + " "
                else:
                    output += str(posHor) + ""
            output += " |\n"
        output += "_____________________________\n"
        return output

    def getPos(self, x, y):
        return self.matrix[y][x]

    def setPos(self, x, y, value):
        self.matrix[y][x] = value

    def getFreePos(self):
        emptyZones = []
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    c = Coord(j, i)
                    emptyZones.append(c)
        if len(emptyZones) > 0:
            #print "----- Empty zones -----"
            #for zone in emptyZones:
            #    print zone
            #print "-----------------------"
            return emptyZones[random.randint(0,len(emptyZones)-1)]
        else:
            return None

    def checkWinner(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 2048:
                    return True
        return False

    def availableMov(self):
        for i in range(4):
            for j in range(4):
                try:
                    if (self.matrix[i][j] == self.matrix[i][j+1]) or \
                       (self.matrix[i][j] == self.matrix[i+1][j]):
                        return True
                except IndexError:
                    pass
        return False


    def getGameState(self):
        if self.checkWinner():
            return 'win'
        elif self.getFreePos() != None:
            return 'ok'
        elif self.availableMov():
            return 'ok'
        else:
            return 'lose'


    def moveRigthOrLeft(self, mov):
        """
        Indicate if the movement is rigth or left with 'r' or 'l'
        Return true if do any movement
        """
        moveDone = False
        if mov is 'r':
            movement = [3, 2, 1, 0]
        else:
            movement = range(4)
        for posy in range(4):
            queueEmpty = deque([])
            prevN = {'pos': -1, 'val': -1}
            for posx in movement:
                if self.matrix[posy][posx] == 0:
                    queueEmpty.append(posx)
                elif self.matrix[posy][posx] != 0:
                    if prevN['val'] == self.matrix[posy][posx]:
                        self.matrix[posy][prevN['pos']] *= 2
                        self.matrix[posy][posx] = 0
                        prevN['val'] = -1
                        prevN['pos'] = -1
                        queueEmpty.append(posx)
                        moveDone = True
                    else:
                        if len(queueEmpty) > 0:
                            newPos = queueEmpty.popleft()
                            self.matrix[posy][newPos] = self.matrix[posy][posx]
                            self.matrix[posy][posx] = 0
                            queueEmpty.append(posx)
                            prevN['val'] = self.matrix[posy][newPos]
                            prevN['pos'] = newPos
                            moveDone = True
                        else:
                            prevN['val'] = self.matrix[posy][posx]
                            prevN['pos'] = posx
                else:
                    pass
        return moveDone



    def moveUpOrDown(self, mov):
        """
        Indicate if the movement is up or down with 'u' or 'd'
        Return true if do any movement
        """
        moveDone = False
        if mov is 'u':
            movement = range(4)
        else:
            movement = [3, 2, 1, 0]
        for posx in range(4):
            queueEmpty = deque([])
            prevN = {'pos': -1, 'val': -1}
            for posy in movement:
                if self.matrix[posy][posx] == 0:
                    queueEmpty.append(posy)
                elif self.matrix[posy][posx] != 0:
                    if prevN['val'] == self.matrix[posy][posx]:
                        self.matrix[prevN['pos']][posx] *= 2
                        self.matrix[posy][posx] = 0
                        prevN['val'] = -1
                        prevN['pos'] = -1
                        queueEmpty.append(posy)
                        moveDone = True
                    else:
                        if len(queueEmpty) > 0:
                            newPos = queueEmpty.popleft()
                            self.matrix[newPos][posx] = self.matrix[posy][posx]
                            self.matrix[posy][posx] = 0
                            queueEmpty.append(posy)
                            prevN['val'] = self.matrix[newPos][posx]
                            prevN['pos'] = newPos
                            moveDone = True
                        else:
                            prevN['val'] = self.matrix[posy][posx]
                            prevN['pos'] = posy
                else:
                    pass
        return moveDone


def generateNum():
    """
    Generate in a proportion of 7 '4' for 10 '2' and choose one
    """
    list2 = [2 for i in range(10)]
    list4 = [4 for i in range(7)]
    list2.extend(list4)
    random.shuffle(list2)
    return list2.pop()


if __name__ == '__main__':
    # Create the board
    board = Board()
    print "write 8 (up), 2 (down), 4 (left), 6 (rigth)"
    while board.getFreePos() != None:
        moveDone = False
        pos = board.getFreePos()
        num = generateNum()
        board.setPos(pos.x, pos.y, num)
        print board

        while not moveDone:
            mov = raw_input(">> ")
            if (mov is '8'):
                moveDone = board.moveUpOrDown('u')
            elif (mov is '2'):
                moveDone = board.moveUpOrDown('d')
            elif (mov is '4'):
                moveDone = board.moveRigthOrLeft('l')
            elif (mov is '6'):
                moveDone = board.moveRigthOrLeft('r')
            else:
                print "must be '8', '2', '4' or '6'"
            if not moveDone:
                print "Invalid movement"
