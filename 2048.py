#!/usr/bin/env python
from logic2048 import Board, generateNum
import Tkinter as tk
import tkMessageBox

BACKGROUND_COLOR = "#BBADA0"
CELL_COLOR = "#CBC2B3"
GRID_LENGTH = 4
TABLE_SIZE = 400
TILE_PADDING = 6
NUM_COLORS = {0: '#CBC2B3', 2: '#EEE6DB', 4: '#ECE0C8', 8: '#EFB27C',
              16: '#F39768', 32: '#ED805B', 64: '#F46042', 128: '#EACF76',
              256: '#EDCB66', 512: '#E8CA53', 1024: '#E7C257', 2048: '#ECC400',
              4096: '#ECC400', 8192: '#ECC400', 16384: '#ECC400', 32768: '#ECC400',
              65536: '#ECC400', 131072: '#ECC400', 262144: '#ECC400', 524288: '#ECC400'}

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.master.title('2048 game')
        self.master.bind("<Key>", self.keyPressed)
        
        self.tiles = []
        self.board = Board()
        self.initGrid()
        self.startGame()


    def initGrid(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        table = tk.Frame(self, bg=BACKGROUND_COLOR, width=500, height=500)
        table.grid(row=0, column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        for column in range(GRID_LENGTH):
            self.tiles.append([])
            for row in range(GRID_LENGTH):
                gridCell = tk.Frame(table, height=TABLE_SIZE/GRID_LENGTH, width=TABLE_SIZE/GRID_LENGTH)
                gridCell.grid(row=row, column=column, padx=TILE_PADDING, pady=TILE_PADDING)
                tile_txt = tk.Label(gridCell, text="", justify='center', font=("Arial", 30, 'bold'), width=4, height=2, bg=CELL_COLOR)
                tile_txt.grid()
                self.tiles[column].append(tile_txt)

    def updateCells(self):
        for row in range(GRID_LENGTH):
            for column in range(GRID_LENGTH):
                num = self.board.getPos(row, column)
                if num == 0:
                    self.tiles[row][column].configure(text='', bg=NUM_COLORS[num])
                else:
                    self.tiles[row][column].configure(text=str(num), bg=NUM_COLORS[num])
        self.update_idletasks()

    def keyPressed(self, ev):
        moveDone = False
        key = ev.char

        if (key is '8' or key is 'w'):
            moveDone = self.board.moveUpOrDown('u')
        elif (key is '2' or key is 's'):
            moveDone = self.board.moveUpOrDown('d')
        elif (key is '4' or key is 'a'):
            moveDone = self.board.moveRigthOrLeft('l')
        elif (key is '6' or key is 'd'):
            moveDone = self.board.moveRigthOrLeft('r')

        self.updateCells()
        if moveDone:
            state = self.board.getGameState()
            if state == 'win':
                print 'win'
                tkMessageBox.showinfo("Win", "You win :)")
            elif state == 'lose':
                print 'lose'
                tkMessageBox.showinfo("Lose", "You lost :(")
            elif state == 'ok':
                pos = self.board.getFreePos()
                num = generateNum()
                self.board.setPos(pos.x, pos.y, num)
                self.updateCells()
                if self.board.getGameState() == 'lose':
                    print 'lose'
                    tkMessageBox.showinfo("Lose", "You lost :(")
            else:
                raise Exception('Uncaught game state: ' + str(state))


    def startGame(self):
        pos = self.board.getFreePos()
        num = generateNum()
        self.board.setPos(pos.x, pos.y, num)
        self.updateCells()


if __name__ == '__main__':
    app = Game2048()
    app.mainloop()
