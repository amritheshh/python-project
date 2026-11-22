
def display_board(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def move(board,player,ch):
    while True:
        position = input(f"Player {player} ({ch}), choose a cell from 1 to 9: ").strip()
        if position=="":
           print(" enter a cell number")
           continue

        if not position.isdigit():
            print("Enter a number.")
            continue

        position=int(position)

        if position < 1 or position > 9:
            print("enter a number between 0 and 8")
            continue
        
        position = position-1

        if board[position] != " ":
            print("That cell is already taken. Choose an empty cell.")
            continue
        return position

def winner(board, ch):
    lines = [
        [0, 1, 2],  
        [3, 4, 5],  
        [6, 7, 8],  
        [0, 3, 6],  
        [1, 4, 7], 
        [2, 5, 8],  
        [0, 4, 8], 
        [2, 4, 6] 
        ]
    for i in lines:
        if (board[i[0]]==ch and board[i[1]]==ch and board[i[2]]==ch):
            return True
    return False


def main():
    board = [" "] * 9
    print("start the game ")
    player = 1
    ch = "x"
    while True:
        display_board(board)
        position = move(board, player, ch)
        board[position] = ch
    
        if winner(board, ch):
            display_board(board)
            print(f"Player {player} ({ch}) wins!")
            break
        
        if " " not in board:
            display_board(board)
            print("It's a draw!")
            break

        if player==1:
            player = 2
            ch= "o"
        else:
            player = 1
            ch ="x"

while True:
    main()
    again = input("Would you like to play again? (yes/no): ").strip().lower()
    if again == "no":
        print("Thanks for playing!")
        break