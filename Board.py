class Board:
    Boardboard = [0]
    def __init__(self,ColNum):
        self.board = [[0] * ColNum for num in range(ColNum)]
        self.startCol = ColNum//2 -1
        self.startRow = ColNum//2 -1
        # 白色的是o，黑色的是x，未被占用是. .用0表示，x用-1表示，o用1表示
        self.board[self.startRow][self.startCol] = 1
        self.board[self.startRow][self.startCol+1] = -1
        self.board[self.startRow+1][self.startCol] = -1
        self.board[self.startRow + 1][self.startCol + 1] = 1

    def getdata(self):
        return self.board
