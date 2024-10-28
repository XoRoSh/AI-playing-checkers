import argparse
import copy
from curses.ascii import isupper
import sys
import time

cache = {} # you can use this to implement state caching

maxValue = 100000000 
minValue = -100000000
debugging = False 

def is_in_bounds(r, c): 
    if r < 0 or r >= 8 or c < 0 or c >= 8: 
        if (debugging): 
            print("Hitting boundaries")
        return False  
    return True

def evaluate_piece(piece):
    if piece == "r":
        return 1
    if piece == "b":
        return -1
    if piece == "R": 
        return 2
    if piece == "B": 
        return -2
    return 0

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):
        self.board = board
        self.width = 8
        self.height = 8
    # function to evaluate table score 


def heuristic_state(board): 
    score = 0
    for i in board:
        for j in i:
            add =  evaluate_piece(j)
            if add != 0: 
               if i == 7 or j == 7 or i == 0 or j == 0: 
                add += 0.2
            score += add
    return score 

def display(board):
    for i in board:
        for j in i:
            print(j, end="")
        print("")
    print("")



def simple_move(board, r, c, newr, newc, is_red): 
    piece = board[r][c]
    if(not is_in_bounds(newr, newc)):
        return None 
    piece_up_right = board[newr][newc]

    if (piece_up_right == "."):
        newBoard = copy.deepcopy(board)
        newBoard[newr][newc] = piece
        newBoard[r][c] = "." 

        if is_red: 
            make_red_king(newBoard, newr, newc)
        else: 
            make_black_king(newBoard, newr, newc)

        return newBoard 
    else: 
        return 

def move_up_right(board, r, c): 
    newr = r - 1
    newc = c + 1
    return simple_move(board, r, c, newr, newc, True)


def move_up_left(board, r, c): 
    newr = r - 1
    newc = c - 1
    return simple_move(board, r, c, newr, newc, True)

def move_down_right(board, r, c ):
    newr = r + 1
    newc = c + 1
    return simple_move(board, r, c, newr, newc, False)

def move_down_left(board, r, c):
    newr = r + 1
    newc = c - 1
    return simple_move(board, r, c, newr, newc, False)




def jump_if_can(current_board, r, c, player, is_first):
    jumping_successors = []
    new_board_right = copy.deepcopy(current_board)
    new_board_left = copy.deepcopy(current_board)
    has_jumped = False
    
    if is_first == False: 
        if player == "r" and r == 2: # TODO: STILL CAN JUMP BUT NOT UPWARDS
            jumping_successors = jump_red_make_king(new_board_right, r, c)
            return jumping_successors
        elif player == "b" and r == 5:# TODO: STILL CAN JUMP BUT NOT DOWNWARDS
            jumping_successors = jump_black_make_king(new_board_right, r, c)
            return jumping_successors
        else: 
            new_board_down_left = copy.deepcopy(current_board)
            new_board_down_right = copy.deepcopy(current_board)

            jumped = jump_up_right(new_board_right, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r - 2, c + 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  

            jumped = jump_up_left(new_board_left, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r - 2, c - 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  
                    
            jumped = jump_down_right(new_board_down_right, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r + 2, c + 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  
            
            jumped = jump_down_left(new_board_down_left, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r + 2, c - 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  


    elif player == "r":
        if r == 2: 
            jumping_successors = jump_red_make_king(new_board_right, r, c)
            return jumping_successors
        else:
            jumped = jump_up_right(new_board_right, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r - 2, c + 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  
            
            jumped = jump_up_left(new_board_left, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r - 2, c - 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  

    elif player == "b":
        if r == 5:
            jumping_successors = jump_black_make_king(new_board_right, r, c)
            return jumping_successors
        else:
            jumped = jump_down_right(new_board_right, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r + 2, c + 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  
            
            jumped = jump_down_left(new_board_left, r, c)
            if jumped is not None:
                has_jumped = True
                successors = jump_if_can(jumped, r + 2, c - 2, player, False)
                if not successors: 
                    jumping_successors.append(jumped)
                else: 
                    jumping_successors.extend(successors)  

    if has_jumped == False:
        if jumped is not None: 
            print("DOBAVLAYU NAHUI")
            jumping_successors.append(jumped)

    return jumping_successors 


def jump_up_right(board, r, c): 
    rOpp, cOpp = r - 1, c + 1
    rTo, cTo = r - 2, c + 2 
    return simple_jump(board, r, c, rOpp, cOpp, rTo, cTo)

def jump_up_left(board, r, c): 
    rOpp, cOpp = r - 1, c - 1
    rTo, cTo = r - 2, c - 2 
    return simple_jump(board, r, c, rOpp, cOpp, rTo, cTo)
    
def jump_down_right(board, r, c): 
    rOpp, cOpp = r + 1, c + 1
    rTo, cTo = r + 2, c + 2 
    return simple_jump(board, r, c, rOpp, cOpp, rTo, cTo)

def jump_down_left(board, r, c): 
    rOpp, cOpp = r + 1, c - 1
    rTo, cTo = r + 2, c - 2 
    return simple_jump(board, r, c, rOpp, cOpp, rTo, cTo)

def simple_jump(board, r, c, rOpp, cOpp, rTo, cTo):  
    piece = board[r][c]

    if is_in_bounds(r, c) and is_in_bounds(rOpp, cOpp) and is_in_bounds(rTo, cTo): 
        piece_up_right = board[rOpp][cOpp]
        dest = board[rTo][cTo]
        if(dest == ".") and piece_up_right in get_opp_char(piece):
            board[rOpp][cOpp] = "." 
            board[rTo][cTo] = piece 
            board[r][c] = "." 
            return board
    return None


def jump_red_make_king(board, r, c): 
    successors = []
    right_board =  board
    left_board = copy.deepcopy(board)
    jumped = jump_up_right(right_board, r, c) 
    if jumped is not None: 
        jumped[r-2][c+2] = jumped[r-2][c+2].upper()
        successors.append(jumped)
    jumped = jump_up_left(left_board, r, c) 
    if jumped is not None: 
        jumped[r-2][c-2] = jumped[r-2][c-2].upper()
        successors.append(jumped)
    return successors


def jump_black_make_king(board, r, c): 
    successors = []
    right_board =  board
    left_board = copy.deepcopy(board)
    jumped = jump_down_right(right_board, r, c) 
    if jumped is not None: 
        jumped[r+2][c+2] = jumped[r+2][c+2].upper()
        successors.append(jumped)
    jumped = jump_down_left(left_board, r, c) 
    if jumped is not None: 
        jumped[r+2][c-2] = jumped[r+2][c-2].upper()
        successors.append(jumped)
    return successors



   
def game_over(board): 
    countRed = 0
    countBlack = 0
    for i in board:
        for j in i:
            if (j == "b" or j == "B"):
                countBlack += 1
            elif (j == "r" or j == "R"):
                countRed += 1
    if (countRed > 0 and countBlack ==0):
        return True
    if (countBlack > 0 and countRed ==0): 
        return True
    return False

    
def play_game(initial_board, depth, output_file):
    current_board = copy.deepcopy(initial_board)

    is_game_over = False
    is_maximizing_player = True  

    with open(output_file, 'w') as f:
        sys.stdout = f
        display(initial_board)
        while not is_game_over:
            
            if is_maximizing_player:
                _, best_move = minmax(current_board, depth, True, float('-inf'), float('inf'))

            else:
                _, best_move = minmax(current_board, depth, False, float('-inf'), float('inf'))

            if best_move is None:
                break

            current_board = best_move  # Update the board to the best move
            display(current_board)

            is_game_over = game_over(current_board)
            if is_game_over:
                break

            is_maximizing_player = not is_maximizing_player





def minmax(board, depth, is_maximizing_player, alpha, beta):
    current_boad = copy.deepcopy(board)
    if game_over(board): 
        return 1234567890, board

    if depth == 0:
        return heuristic_state(board), board
    
    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        successors = generate_successors(current_boad, 'r')
        if not successors:
            return game_over(current_boad), current_boad
        for successor in successors:



            eval, _ = minmax(successor, depth - 1, False, alpha, beta)

            if eval > max_eval:
               max_eval = eval
               best_move = successor

            alpha = max(alpha, eval)
            if alpha >= beta:
                break  

        return max_eval, best_move
    else:
        min_eval = float('inf')
        successors = generate_successors(current_boad, 'b')
        if not successors: 
            game_over(current_boad)
        for successor in successors: 
            eval, _ = minmax(successor, depth - 1, True, alpha, beta)

            # print("Display:")
            # display(successor)
            if eval <= min_eval: 
                min_eval = eval
                best_move = successor

            beta = min(beta, eval)
            if alpha >= beta:
                break  
        return min_eval, best_move


def generate_successors(board, player):
    successors = []
    current_board = board
    if player.lower() == "r": 
        # Jumping 
        for r in range(8):
            for c in range(8):
                piece = current_board[r][c]
                if piece == "r":
                    if (debugging):
                        print("PIECE ")
                    # Try moving in all directions based on the piece and player
                    successors += jump_if_can(current_board, r, c, "r", True)
                    if (debugging): 
                        print("returned successor: ")
                        for board in successors: 
                            if board != None: 
                                display(board)
                            else: 
                                print("no jumping options")
                if piece == "R": 
                    successors += jump_if_can(current_board, r, c, "R", False)
        # Simple moves
        if not successors: 
            if (debugging): 
                print("SIMPLE MOVE")
            for r in range(8): 
                for c in range(8):
                    piece = current_board[r][c] 
                    if piece == "R": 
                        successors += generate_kings_simple_successors(current_board, r, c)

                        if (debugging):
                            for board in successors: 
                                print("Kings Successor: ")
                                display(board)
                    if piece == "r": 
                        if (debugging): 
                            print("PIECE")
                        successors += generate_simple_successors_red(current_board, r, c) 
                        if (debugging): 
                            for board in successors: 
                                print("Successor: ")
                                display(board)
    else: 
        # Jumping 
        for r in range(8):
            for c in range(8):
                piece = current_board[r][c]
                if piece == "b":
                    if (debugging):
                        print("BLACK PIECE ")
                    # Try moving in all directions based on the piece and player
                    successors += jump_if_can(current_board, r, c, "b", True)
                    if (debugging): 
                        print("returned successor: ")
                        for board in successors: 
                            if board != None: 
                                display(board)
                            else: 
                                print("no jumping options")
                if piece == "B": 
                    if (debugging): 
                        print("Black KING")
                    successors += jump_if_can(current_board, r, c, "B", False)
        # Simple moves
        if not successors: 
            if (debugging): 
                print("SIMPLE MOVE")
            for r in range(8): 
                for c in range(8):
                    piece = current_board[r][c] 
                    if piece == "B": 
                        successors += generate_kings_simple_successors(current_board, r, c)

                        if (debugging):
                            for board in successors: 
                                print("Kings Successor: ")
                                display(board)
                    if piece == "b": 
                        successors += generate_simple_successors_black(current_board, r, c) 
                        if (debugging): 
                            for board in successors: 
                                print("Successor: ")
                                display(board)
    return successors 



def make_red_king(board, r, c): 
    if r == 0:
        if board[r][c].islower(): 
            board[r][c] = "R"
    return board

def make_black_king(board, r, c): 
    if r == 7:
        if board[r][c].islower(): 
            board[r][c] = "B"
    return board

def generate_simple_successors_red(board, r, c): 
    simple_successors = []
    res = move_up_right(board, r, c)
    if res is not None: 
        simple_successors.append(res)

    res = move_up_left(board, r, c)
    if res is not None: 
        simple_successors.append(res)
    return simple_successors


def generate_simple_successors_black(board, r, c): 
    simple_successors = []
    res = move_down_right(board, r, c)
    if res is not None: 
        simple_successors.append(res)

    res = move_down_left(board, r, c)
    if res is not None: 
        simple_successors.append(res)
    return simple_successors

def generate_kings_simple_successors(board, r, c): 
    kings_simple_successors = []
    kings_simple_successors += generate_simple_successors_black(board, r, c)
    kings_simple_successors += generate_simple_successors_red(board, r, c)
    return kings_simple_successors



def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    # python3 checkers_starter.py --inputfile checkers1.txt --outputfile checkersO1.txt-
    turn = 'r'
    row = 7 
    column = 0 

    # state.board[7][6] = "R"
    # state.board[6][5] = "b"
    # state.board[4][3] = "b"
    # state.board[2][3] = "b"
    # state.board[6][3] = "b"
    # state.board[4][5] = "b"


    # state.board[7][5] = "r"
    # state.board[6][6] = "b"
    # state.board[4][6] = "b"
    # state.board[4][4] = "b"
    # state.board[2][6] = "b"
    # state.board[4][2] = "b"

    # state.board[7][0] = "r"
    # state.board[6][1] = "b"
    # state.board[4][3] = "b"
    # state.board[2][5] = "b"

    # state.board[7][7]= "r"
    # state.board[6][6]= "b"
    # state.board[4][4]= "b"
    # state.board[2][2]= "b"

    # state.board[5][3] = "R"
    # state.board[4][2] = "b"
    # state.board[4][4] = "b"
    # state.board[6][2] = "b"
    # state.board[6][4] = "b"
    # state.board[2][4] = "b"

# # RED BECOMING KING
#     state.board[1][2]= "b"
#     state.board[1][4]= "b"
#     state.board[2][3]= "r"

# # RED BECOME KING HARD 
#     state.board[6][7]= "r"
#     state.board[5][6]= "b"
#     state.board[3][4]= "b"
#     state.board[1][2]= "b"
#     state.board[1][4]= "b"

###### TESTING BLACK

    # # Simple move
    # state.board[2][2]= "b"

    # # Black King simple
    # state.board[6][2]= "b"



    # #Black simple jump 
    # state.board[3][2]= "b"
    # state.board[4][1]= "r"
    # state.board[4][3]= "r"


    # # Black multijump
    # state.board[1][0]= "b"
    # state.board[2][1]= "r"
    # state.board[4][3]= "r"
    # state.board[6][5]= "r"

    # #Black hard jump 
    # state.board[2][2]= "b"
    # state.board[3][1]= "r"
    # state.board[3][3]= "r"
    # state.board[3][5]= "r"
    # state.board[1][5]= "r"
    # state.board[5][5]= "r"


    # print("initial: ")
    # display(state.board)
    # successors = generate_successors(state, "r")
    # print("ALL SUCCESSORS")
    # for successor in successors: 
    #     display(successor)
    # print(f"Number of successors: {len(successors)}")


    # minmax(state.board, 2, True, -999999999, 999999999)


    sys.stdout = open(args.outputfile, 'w')
    play_game(state.board, 10, args.outputfile)
