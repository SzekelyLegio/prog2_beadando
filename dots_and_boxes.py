# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 20:20:11 2020

@author: HargitaiFenegyerek
"""
from tkinter import *
import numpy as np


symbol_thickness = 50

player1_color = '#F57001'
player1_color_light = '#FF7F40'
player2_color = '#F50101'
player2_color_light = '#F4815F'
Green_color = '#A2FF40'



class Dots_and_Boxes():
    #Inicializáljuk az ablakot
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=returnSizeOfBoard(), height=returnSizeOfBoard())
        self.canvas.pack()

        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.newGame()


    def newGame(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(getDots() - 1, getDots() - 1))
        self.row_status = np.zeros(shape=(getDots(), getDots() - 1))
        self.col_status = np.zeros(shape=(getDots() - 1, getDots()))

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.bottomTextChanger()

    def mainloop(self):
        self.window.mainloop()


    #Ellenőrzi , hogy már ráklikkeltek e az adott vonalra
    def check_foglalt(self, logPos, type):
        r = logPos[0]
        c = logPos[1]
        foglalt = True
        if type == 'row' and self.row_status[c][r] == 0:
            foglalt = False
        if type == 'col' and self.col_status[c][r] == 0:
            foglalt = False
        return foglalt

    #A klikkelt helyet konvertálja logikai pozícióvá
    def clickToLogicalPosition(self, packPos):
        packPos = np.array(packPos)
        position = (packPos-returnDistance()/4)//(returnDistance()/2)
        type = False
        logPos = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logPos = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logPos = [r, c]
            type = 'col'

        return logPos, type

    #Megnézi hogy megvan e a 4 oldal jelölve és ha igen a 4 oldal között beszinezi a player szinével
    def fillBoxes(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                print("boxcolored")
                start_x = returnDistance() / 2 + box[1] * returnDistance() + returnEdgeWidth() / 2
                start_y = returnDistance() / 2 + box[0] * returnDistance() + returnEdgeWidth() / 2
                end_x = start_x + returnDistance() - returnEdgeWidth()
                end_y = start_y + returnDistance() - returnEdgeWidth()
                self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = player2_color_light
                print("boxcolored")
                start_x = returnDistance() / 2 + box[1] * returnDistance() + returnEdgeWidth() / 2
                start_y = returnDistance() / 2 + box[0] * returnDistance() + returnEdgeWidth() / 2
                end_x = start_x + returnDistance() - returnEdgeWidth()
                end_y = start_y + returnDistance() - returnEdgeWidth()
                self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def update_board(self, type, logPos):
        r = logPos[0] # sor
        c = logPos[1] # oszlop
        val = 1
        if self.player1_turn:
            val =- 1
        if c < (getDots()-1) and r < (getDots()-1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()


    #megrajzolja a dolgokat
    def DrawclickLine(self, type, logPos):
        if type == 'row':
            start_x = returnDistance()/2 + logPos[0]*returnDistance()
            end_x = start_x+returnDistance()
            start_y = returnDistance()/2 + logPos[1]*returnDistance()
            end_y = start_y
        elif type == 'col':
            start_y = returnDistance() / 2 + logPos[1] * returnDistance()
            end_y = start_y + returnDistance()
            start_x = returnDistance() / 2 + logPos[0] * returnDistance()
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=returnEdgeWidth())

    # Játék végén game over képernyő
    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            text = 'Győztes: ' +getPalyerName()
            color = player1_color
        elif player2_score > player1_score:
            text = 'Győztes: ' + getPalyerName2()
            color = player2_color
        else:
            text = 'DÖNTETLEN'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(returnSizeOfBoard() / 2, returnSizeOfBoard() / 3,  fill=color, text=text)

        score_text = 'Pontok: \n'
        self.canvas.create_text(returnSizeOfBoard() / 2, 5 * returnSizeOfBoard() / 8, fill=Green_color,
                                text=score_text)

        score_text = getPalyerName() + str(player1_score) + '\n'
        score_text += getPalyerName2() + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(returnSizeOfBoard() / 2, 3 * returnSizeOfBoard() / 4, fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Új játék \n'
        self.canvas.create_text(returnSizeOfBoard() / 2, 15 * returnSizeOfBoard() / 16, fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(getDots()):
            x = i*returnDistance()+returnDistance()/2
            self.canvas.create_line(x, returnDistance()/2, x,
                                    returnSizeOfBoard()-returnDistance()/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(returnDistance()/2, x,
                                    returnSizeOfBoard()-returnDistance()/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(getDots()):
            for j in range(getDots()):
                start_x = i*returnDistance()+returnDistance()/2
                end_x = j*returnDistance()+returnDistance()/2
                self.canvas.create_oval(start_x-returnDotWidth()/2, end_x-returnDotWidth()/2, start_x+returnDotWidth()/2,
                                        end_x+returnDotWidth()/2, fill=returnDotColor(),
                                        outline=returnDotColor())


    # Az alsó szöveg változtatgatása
    def bottomTextChanger(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += getPalyerName()
            color = player1_color
        else:
            text += getPalyerName2()
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(returnSizeOfBoard() - 5*len(text),
                                                       returnSizeOfBoard()-returnDistance()/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def click(self, event):
        if not self.reset_board:
            packPos = [event.x, event.y]
            logical_positon, valid_input = self.clickToLogicalPosition(packPos)
            if valid_input and not self.check_foglalt(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.DrawclickLine(valid_input, logical_positon)
                self.fillBoxes()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.bottomTextChanger()
        else:
            self.canvas.delete("all")
            self.newGame()
            self.reset_board = False



def set_Dots():
    dots = int(e3.get())


def getDots():
    return int(e3.get())

def getPalyerName():
    return e1.get()
def getPalyerName2():
    return e2.get()

def start_game():
    if getDots() != 0 and getPalyerName() != '' and getPalyerName2() != '':
        game_instance = Dots_and_Boxes()
        game_instance.mainloop()

        window2.destroy()
def returnDistance():

    return getDots()*100 / (getDots())

def returnEdgeWidth():
    return 0.2 * getDots()*100 /  getDots()


def returnSizeOfBoard():
    return  getDots()*100

def returnSymbolSize():
    return (returnSizeOfBoard() / 3 - returnSizeOfBoard() / 8) / 2
def returnDotWidth():
    return 0.2 * returnSizeOfBoard() / getDots()
def returnDotColor():
            return '#FA0000'


window2 = Tk()
window2.title('Setup window')
l1= Label(window2,text ="Player1")
l1.grid(row = 0, column = 0)

l2= Label(window2,text ="Player 2")
l2.grid(row = 1, column = 0)

l3= Label(window2,text ="Pontok száma")
l3.grid(row = 0, column = 2)
player=StringVar()

e1=Entry(window2,textvariable=player)
e1.grid(row=0, column= 1)


player2=StringVar()
e2=Entry(window2,textvariable=player2)
e2.grid(row=1, column= 1)
myDotSize = IntVar()
e3=Entry(window2,textvariable=myDotSize)
e3.grid(row=0, column= 3)
b1=Button(window2,text="setDots",width=13 ,command =set_Dots)
b1.grid(row =1 , column = 2)
b2=Button(window2,text="StartGame",width=13 ,command =start_game)
b2.grid(row =1 , column = 3)

window2.mainloop()