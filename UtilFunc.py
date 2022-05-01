import Board
from Board import *
import datetime
import time
from copy import deepcopy
from MCTS import *
def printBoard(board):
    l = len(board)
    print(' ', end = ' ')
    for i in range(l):
        print(chr(ord('a') + i), end = ' ')
    print()
    for i in range(l):
        print(chr(ord('a') + i), end = ' ')
        for j in range(l):
            if (board[i][j] == 0):
                print('.', end = ' ')
            elif (board[i][j] == -1):
                print('X', end = ' ')
            else:
                print('O', end = ' ')
        print()


def flip(row,col,color):
    Board.Boardboard[row][col] = color
    direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    rowLen = len(Board.Boardboard[0])
    colLen = len(Board.Boardboard[1])
    for dx,dy in direction:
        tempRow = row
        tempCol = col
        x,y = row+dx,col+dy
        while(0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == -color):
            x += dx
            y += dy
            if(0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == color):
                while(tempRow !=x or tempCol !=y):
                    tempRow += dx
                    tempCol += dy
                    Board.Boardboard[tempRow][tempCol] = color

def flip_sim(board,row,col,color):
    board[row][col] = color
    direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    rowLen = len(board[0])
    colLen = len(board[1])
    for dx,dy in direction:
        tempRow = row
        tempCol = col
        x,y = row+dx,col+dy
        while(0 <= x < rowLen and 0 <= y < colLen and board[x][y] == -color):
            x += dx
            y += dy
            if(0 <= x < rowLen and 0 <= y < colLen and board[x][y] == color):
                while(tempRow !=x or tempCol !=y):
                    tempRow += dx
                    tempCol += dy
                    board[tempRow][tempCol] = color

def check_legal_move(color):
    accessPos = []
    # 表示棋盘坐标点的8个不同方向坐标
    direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    rowLen = len(Board.Boardboard[0])
    colLen = len(Board.Boardboard[1])
    for i in range(rowLen):
        for j in range(colLen):
            if (Board.Boardboard[i][j] == color):
                for dx, dy in direction:
                    x, y = i + dx, j + dy
                    if(0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == -color):
                        while (0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == -color):
                            x += dx
                            y += dy
                        if (0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == 0 and [x,y] not in accessPos):
                            accessPos.append([x, y])
                    # if (0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] == -color):
                    #     while (0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] != 0 ):
                    #         x += dx
                    #         y += dy
                    #     if(0 <= x < rowLen and 0 <= y < colLen and Board.Boardboard[x][y] != color):
                    #         accessPos.append([x, y])
    return accessPos

def check_legal_move_sim(board,color):
    accessPos = []
    # 表示棋盘坐标点的8个不同方向坐标
    direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    rowLen = len(board[0])
    colLen = len(board[1])
    for i in range(rowLen):
        for j in range(colLen):
            if (board[i][j] == color):
                for dx, dy in direction:
                    x, y = i + dx, j + dy
                    if(0 <= x < rowLen and 0 <= y < colLen and board[x][y] == -color):
                        while(0 <= x < rowLen and 0 <= y < colLen and board[x][y] == -color):
                            x += dx
                            y += dy
                        if(0 <= x < rowLen and 0 <= y < colLen and board[x][y] == 0 and [x,y] not in accessPos):
                            accessPos.append([x, y])
    return accessPos

def computer_move(color):
    chr_color = 'X' if(color == -1) else 'O'
    accessPos = check_legal_move(color)
    if (len(accessPos) == 0):
        print("{0}玩家已经没有位置可以下了！".format('X' if color == -1 else 'o'))
        return -1
    else:
        ai = AIPlayer(chr_color)
        board = deepcopy(Board.Boardboard)
        action = ai.get_move(board)
        flip(action[0], action[1], color)
        row = chr(action[0] +ord('a'))
        col = chr(action[1] +ord('a'))
        print("computer place {0} at: {1}{2}".format('X'if color== -1 else 'o',row,col))
        return 1

def human_move(color):
    accessPos = check_legal_move(color)
    if (len(accessPos) == 0):
        print("{0}玩家已经没有位置可以下了！".format('X' if color == -1 else 'o'))
        return -1
    else:
        RowCol = input("Enter move for {0} (RowCol): ".format('X'if color==-1 else 'o'))
        #利用ascii码直接计算行列值
        row = ord(RowCol[0]) - ord('a')
        col = ord(RowCol[1]) - ord('a')
        assert [row,col] in accessPos,"你的落子位置非法，游戏结束！"
        flip(row,col,color)
        return 1

def gameover(computerColor,humanColor):                                          #游戏结束判定
    xplayer = "Computer" if(computerColor == -1) else "Human"
    oplayer = "Human" if(humanColor == 1) else "Computer"
    onum,xnum,winner,_ = getWinner()
    if(winner == 0):
        print("{0} 赢了!".format(xplayer))
        print("X : O = {0} : {1}".format(xnum, onum))
    elif(winner == 1 ):
        print("{0} 赢了!".format(oplayer))
        print("X : O = {0} : {1}".format(xnum, onum))
    else:
        print("双方平手!")
        print("X : O = {0} : {1}".format(xnum, onum))

def getWinner():
    onum = 0
    xnum = 0
    for i in range(len(Board.Boardboard[0])):
        for j in range(len(Board.Boardboard[1])):
            if (Board.Boardboard[i][j] == -1):
                xnum += 1
            elif (Board.Boardboard[i][j] == 1):
                onum += 1
    if (xnum > onum):
        #x赢
        winner = 0
        dif = xnum - onum
    elif (onum > xnum):
        #y赢
        winner = 1
        dif = onum -xnum
    else:
        #平手
        winner = 2
        dif = xnum-onum
    return onum,xnum,winner,dif


def getWinner_sim(board):
    onum = 0
    xnum = 0
    for i in range(len(board[0])):
        for j in range(len(board[1])):
            if (board[i][j] == -1):
                xnum += 1
            elif (board[i][j] == 1):
                onum += 1
    if (xnum > onum):
        #x赢
        winner = 0
        dif = xnum - onum
    elif (onum > xnum):
        #y赢
        winner = 1
        dif = onum -xnum
    else:
        #平手
        winner = 2
        dif = xnum-onum
    return onum,xnum,winner,dif
def save_info():
 pass
