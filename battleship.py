# References:   https://trinket.io/python/051179b6d3
#               https://codereview.stackexchange.com/questions/232013/a-simple-battleship-game

class BattleShip:
    # keeps ship row and column as well as players secret board and public board.
    def __init__(self):
        self.row = None
        self.col = None
        self.secretBoard = []
        self.publicBoard = []
        self.win = False

    def create_board(self):
        for i in range(6):
            self.secretBoard.append(["0"] * 6)
            self.publicBoard.append(["0"] * 6)

    def print_publicBoard(self):
        for row in self.publicBoard:
            print((" ").join(row))
    
    def print_secretBoard(self):
        for row in self.secretBoard:
            print((" ").join(row))

    # updates as player guesses location
    def update_publicBoard(self, row, col):
        self.publicBoard[row][col] = "X"
    
    def update_secretBoard(self, row, col):
        self.secretBoard[row][col] = "X"
    
    # asks player to set ship
    def initiallizeGame(self):
        print("Lets Play Battleship!")
        print("Let's place your first boat")
        self.row = int(input("Choose your Row (0-5):"))
        self.col = int(input("Choose your Column (0-5): "))
        self.create_board()
        self.update_secretBoard(self.row, self.col)
        print("Great! Here is your secret Board: ")
        self.print_secretBoard()
