# chat-server.py

# References:   https://realpython.com/python-sockets/
#               https://docs.python.org/3.4/howto/sockets.html
#               https://trinket.io/python/051179b6d3
#               https://codereview.stackexchange.com/questions/232013/a-simple-battleship-game

import socket
from battleship import BattleShip

server_arena = BattleShip()


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

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
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        print("Waiting for message....")
        print("Type /q to quit")
        print("Enter message to send. Please wait for input prompt before entering message..")
        print("Note: Client must type 'play battleship' to start a game of battleship.")
        while True:
            #begin chat
            data = conn.recv(1024).decode()
            if(data == "/q"):
                break

            # starts game of battleship
            if(data == "play battleship"):
                server_arena.initiallizeGame()
                print("Now lets guess your apponents board: ")
                server_arena.print_publicBoard()
                print("You have 9 guesses. Try to find your apponents ship before they find yours!")
                
                # 9 rounds to guess servers ship location
                for turn in range(9):
                    print ("Turn", turn)
                    # get coordinates be recieving data and splitting
                    data = conn.recv(1024).decode()
                    sepData = data.split(" ")
                    # print(sepData)
                    clientrow = int(sepData[0])
                    clientcol = int(sepData[1])
                    print(clientrow, clientcol)

                    # check guesses against ship coordinates, send appropiate responses
                    if(clientrow == server_arena.row and clientcol == server_arena.col):
                        print("Client has won the game!")
                        print("Exiting Game")
                        ans = "sunk!"
                        conn.send(ans.encode())
                        # exit game and return to chat
                        break
                    else:
                        ans = "nope"
                        conn.send(ans.encode())

                    # get servers input, validate, and combine to send to client
                    guess_row = getValidInput("Guess Row>")
                    row = int(guess_row)
                    guess_col = getValidInput("Guess Col>")
                    col = int(guess_col)
                    combine = (guess_row, guess_col)
                    sendData = " ".join(combine)
                    conn.send(sendData.encode())

                    # get response
                    resp = conn.recv(1024).decode()
                    if(resp == "sunk!"):
                        print("You Sunk the Ship!")
                        print("Exiting Game.")
                        break
                    else: 
                        print("Missed")
                        server_arena.update_publicBoard(row, col)
                    if turn == 8:
                        print("Game Over")
                    turn =+ 1
                    server_arena.print_publicBoard()

            print(data)
            sendData = input("Enter Input> ")
            conn.send(sendData.encode())
            if(sendData == "/q"):
                break
        conn.close()