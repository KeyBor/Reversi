import datetime
import time
from UtilFunc import *
from Board import *


timeSave = datetime.datetime.now().strftime('%Y-%m-%d %T')  # 保存游戏时间
timeStart = time.time()  # 游戏开始时间
boardLen = int(input('Enter the board dimension：'))  #棋盘的大小
board = Board(boardLen)  # 初始化棋盘
# 在类外初始化类的静态变量，用于全局共享
Board.Boardboard = board.getdata()
computerChess = input('Computer plays (X/O):')  # 保存电脑的棋子
assert computerChess.lower()=='o' or computerChess.lower()=='x',"请输入正确的棋子符号"
printBoard(Board.Boardboard)
computerRes = 0
humanRes = 0
if(computerChess.lower() == 'x'):
    computerTurn = 1
    computerColor = -1
    humanColor = 1
else:
    computerTurn = 0
    computerColor = 1
    humanColor = -1

while(1):
    if(humanRes == -1 and computerRes == -1):
        print("双方玩家都没有合法棋子可以下了！游戏结束")
        gameover(computerColor,humanColor)
        break
    if(computerTurn == 1):
        computerRes = computer_move(computerColor)
        if(computerRes == 1):
            printBoard(Board.Boardboard)
            computerTurn = 0
        elif(computerRes == -1 and humanRes != -1):
            computerTurn = 0
    else:
        humanRes = human_move(humanColor)
        if(humanRes == 1):
            printBoard(Board.Boardboard)
            computerTurn =1
        elif(humanRes == -1 and computerRes != -1):
            computerTurn = 1

