# chat-client.py

# References:   https://realpython.com/python-sockets/
#               https://docs.python.org/3.4/howto/sockets.html
#               https://trinket.io/python/051179b6d3
#               https://codereview.stackexchange.com/questions/232013/a-simple-battleship-game

import socket
from battleship import BattleShip

client_arena = BattleShip()

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# validate user input for game
def getValidInput(prompt):
    while True:
        value = input(prompt)
        if int(value) < 0 or int(value) > 5:
            print("please pick a number between 0-5")
            continue
        else:
            break
    return value

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Type /q to quit.")
    print("Enter message to send. Please wait for input prompt before entering message..")
    print("Note: Type 'play battleship' to start a game of battleship.")
    while True:
        #begin chat
        str = input("Enter Input > ")
        s.send(str.encode())
        if(str == "/q"):
            break
        # starts game of battleship
        if(str == "play battleship"):
            client_arena.initiallizeGame()
            print("Now lets guess your apponents board: ")
            client_arena.print_publicBoard()
            print("You have 9 guesses. Try to find your apponents ship before they find yours!")

            # 9 rounds to guess servers ship location
            for turn in range(9):
                print ("Turn", turn)
                # get coordinates
                guess_row = getValidInput("Guess Row>")
                row = int(guess_row)
                guess_col = getValidInput("Guess Col>")
                col = int(guess_col)

                # combine to send to server
                combine = (guess_row, guess_col)
                data = " ".join(combine)
                print(data)
                s.send(data.encode())

                # recieve responce
                resp = s.recv(1024).decode()
                if(resp == "sunk!"):
                    print("You Sunk the Ship!")
                    print("Exiting Game")
                    break
                else: 
                    print("Missed")
                    client_arena.update_publicBoard(row, col)
                if turn == 8:
                    print("Game Over")
                turn =+ 1
                client_arena.print_publicBoard()

                # servers guess recieved and split into two strings
                sData = s.recv(1024).decode()
                sepData = sData.split(" ")
                # print(sepData)
                serverrow = int(sepData[0])
                servercol = int(sepData[1])
                print(serverrow, servercol)
                
                # check guesses against ship coordinates, send appropiate responses
                if(serverrow == client_arena.row and servercol == client_arena.col):
                    print("Server has won the game!")
                    print("Exiting Game")
                    ans = "sunk!"
                    s.send(ans.encode())
                    # exit game and return to chat
                    break
                else:
                    ans = "nope"
                    s.send(ans.encode())
        data = s.recv(1024).decode()
        if(data == "/q"):
            break
        print(data)

    s.close()