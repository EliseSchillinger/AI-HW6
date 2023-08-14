def create_chess_board():
    """ returns an 'empty' 8x8 2d list ready to add chess pieces """
    board = []
    for row in range(8):
        file = []
        for column in range(8):
            file.append(' ')
        board.append(file)
    return board

def copy_board(chess_board):
    """ copy board for new move generation """
    temp_board = []
    for i in range(len(chess_board)):
        temp_board.append(chess_board[i][:])
    return temp_board

def create_filled_board(FEN):
    """ creates the chess gameboard based on a FEN string
        notes: chess indexing
            rows: 0-7 but in notation it is 8-1, reverse order of our index & w/o zero 
            columns: 0-7 but in notation a-h
    """
    # collect only piece positions from FEN
    index = 0
    piece_locations = FEN.split(' ')
    piece_locations[0] = piece_locations[0].split('/')
    piece_locations = piece_locations[0]

    chess_board = []
    chess_board = create_chess_board()
    # create the board based on said positions: 8x8 board
    for row in range(len(piece_locations)):
        for column in range(len(piece_locations[row])):
            current_location = piece_locations[row][column]

            # if the current location is a number it is empty (based on FEN)
            if current_location.isdigit():
                index += 1
            else:
                chess_board[row][index] = current_location
                index +=1
        index = 0
    return chess_board

def print_board(FEN):
    """ print out the chess board using the FEN """
    chess_board = create_filled_board(FEN)
    file = 8

    print(' ' + '  a b c d e f g h ')
    print('   _______________')
    for row in chess_board:
        print(str(file) + ' |' + str(row).strip("'[']").replace("', '", '|') + '|')
        file -= 1
    print('   ---------------')

# FUNCTIONS FOR READING FEN STRING SEGMENTS ---------------------------------------------------------------------------------------

def split_FEN(my_FEN):
    """ split parts of the FEN into characters """
    return [char for char in my_FEN]

def read_fen_colors(FEN):
    """ determines the color of the AI player and opponent based on the FEN string
    """
    current_FEN = starting_fen.split(' ')
    current_FEN = current_FEN[0]
    current_FEN = current_FEN[0] # do again to determine which color is at the beginning of fen string

    if current_FEN.isupper():
        player_color = 'w'
        opponent_color = 'b'
    else:
        player_color = 'b'
        opponent_color = 'w'
    return player_color, opponent_color

def read_piece_color(piece):
    """color determinator for ANY pieces """
    color = ''
    if piece.isupper():
        color = 'w'
    else:
        color = 'b'
    return color

def read_fen_turn_to_move(FEN):
    """ determines whos turn it is to move based on the FEN string """
    turn_to_move = ''
    current_FEN = FEN.split(' ')
    current_FEN = current_FEN[1]
    if current_FEN == 'w':
        turn_to_move = 'w'
    else:
        turn_to_move = "b"
    return turn_to_move

def read_fen_castle(FEN, player_color):
    """ determines if Castling is possible for either player based on the FEN string
        can be castling for one color or both 
    """
    castle_FEN = ''
    castle_FEN = FEN.split(' ')
    castle_FEN = castle_FEN[2]
    print(castle_FEN)

    castle_options = []
    castle_options = split_FEN(castle_FEN)
    print(castle_options)

    player_castle = ''
    opponent_castle = ''

    for option in castle_options:
        # if there's no castling available
        if option == '-':
            player_castle = '-'
            opponent_castle = '-'
        # all uppercase options
        elif option == 'K' and player_color == 'w':
            player_castle += 'K'
        elif option == 'Q' and player_color == 'w':
            player_castle += 'Q'
        elif option == 'K' and player_color == 'b':
            opponent_castle = 'K'
        elif option == 'Q' and player_color == 'b':
            opponent_castle += 'Q'
        # all lowercase options 
        elif option == 'k' and player_color == 'w':
            opponent_castle += 'k'
        elif option == 'q' and player_color == 'w':
            opponent_castle += 'q'
        elif option == 'k' and player_color == 'b':
            player_castle = 'k'
        elif option == 'q' and player_color == 'b':
            player_castle += 'q'
    
    return player_castle, opponent_castle

def read_fen_en_passant(FEN):
    """ fen segment that determines if en passant is possible 
    """
    player_en_passant = ' '
    player_en_passant = FEN.split(' ')
    player_en_passant = player_en_passant[3]
    
    return player_en_passant

def read_fen_halfmove(FEN):
    """ the number of halfmoves from the FEN string """
    halfmove = 0
    this_fen = ''
    this_fen = FEN.split(' ')
    halfmove = int(this_fen[4])

    return halfmove

def read_fen_fullmove(FEN):
    """ the number of full moves from the FEN string
        incremented after black turn """
    fullmove = 0
    this_fen = ''
    this_fen = FEN.split(' ')
    fullmove = int(this_fen[5])
    return fullmove


# PIECE MOVEMENT FUNCTIONS & RANK-FILE TRANSLATION --------------------------------------------------------------------------------------------

# swapping between 2D list index and rank/file
# maybe just add these into the functions
rows_to_ranks = { 0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1' }
ranks_to_rows = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
files_to_columns = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
columns_to_files = { 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

def get_rank_file(row, column):
    """ return the rank and file from the 2D list index """
    return columns_to_files[column] + rows_to_ranks[row]


def get_2D_index(move):
    """ revert from rank and file back to 2D list indexing - only ending location """
    # alter if necessary
    if len(move) == 4:
        return [ranks_to_rows[move[-1]], files_to_columns[move[-2]]]
    elif len(move) == 5:
        return [ranks_to_rows[move[-2]], files_to_columns[move[-3]]]

def castling(type):
    """ determine the type of castling done and return (in notation for fen string) """
    if type == "K":
        castling_queen = ''
        castling_king = '0-0'
        return castling_queen, castling_king
    else:
        castling_queen = '0-0-0'
        castling_king = ''
        return castling_queen, castling_king

# ----------------------------------------------- tested and works above ------------------------------------------------------------------
def movement_directions (cell, r, step): 
    """ movement through the 2d list using cardinal directions as indicators - alterations for knight movement """
    next_location = cell[:]
    out_of_bounds = False

    # while step is > 0 and in board's bounds: alter the current piece's location based on the ray direction
    while step > 0 and not out_of_bounds:
        if r == 'slide': # used for slide pieces in move determination loops
            continue 
        elif r == 'sw': # southwest
            next_location[0] = next_location[0]+1 # row
            next_location[1] = next_location[1]-1 # column
        elif r == 's': # south
            next_location[0] = next_location[0]+1
        elif r == 'se': # southeast
            next_location[0] = next_location[0]+1
            next_location[1] = next_location[1]+1
        elif r == 'w': # west
            next_location[1] = next_location[1]-1
        elif r == 'e': # east
            next_location[1] = next_location[1]+1
        elif r == 'nw': # northwest
            next_location[0] = next_location[0]-1
            next_location[1] = next_location[1]-1
        elif r == 'n': # north
            next_location[0] = next_location[0]-1
        elif r == 'ne': # northeast
            next_location[0] = next_location[0]-1
            next_location[1] = next_location[1]+1
        # knight specific
        elif r == 'nne': # north north east
            next_location[0] = next_location[0]+1
            next_location[1] = next_location[1]-2
        elif r == 'nee': # north east east
            next_location[0] = next_location[0]+2
            next_location[1] = next_location[1]-1
        elif r == 'see': # south east east
            next_location[0] = next_location[0]+1
            next_location[1] = next_location[1]+2
        elif r == 'sse': # south south east
            next_location[0] = next_location[0]+2
            next_location[1] = next_location[1]+1
        elif r == 'ssw': # south south west
            next_location[0] = next_location[0]+2
            next_location[1] = next_location[1]-1
        elif r == 'sww': # south west west
            next_location[0] = next_location[0]+1
            next_location[1] = next_location[1]-2
        elif r == 'nww': # north west west
            next_location[0] = next_location[0]-1
            next_location[1] = next_location[1]-2
        elif r == 'nnw':# north north west
            next_location[0] = next_location[0]-2
            next_location[1] = next_location[1]-1
            
        # if piece out of board bounds o.o.b becomes true - does not add to move list
        if next_location[0] < 0:
            out_of_bounds = True
        elif next_location[0] > 7:
            out_of_bounds = True
        if next_location[1] < 0:
            out_of_bounds = True
        elif next_location[1] > 7:
            out_of_bounds = True
        step -= 1
    return next_location, out_of_bounds

def generate_moves(chess_board, turn_to_move):
    """ all possible moves regardless of check - except pawns """
    # all possible directions for different pieces
    rays = {'k': ['n','ne', 'e', 'se', 's', 'sw','w', 'nw'],
            'q': ['slide','n','ne', 'e', 'se', 's', 'sw','w', 'nw'],
            'r': ['slide','n', 'e', 's','w'],
            'b': ['slide','ne', 'se', 'sw', 'nw'],
            'n': ['nne','nee', 'see', 'sse', 'ssw', 'sww','nww', 'nnw']
            }

    # variables necessary for piece movement loops and move function - separated for organization purposes
    possible_moves = []
    move, piece, target_piece, capture = '', '', '', ''
    start_row, start_col, end_row, end_col = '', '', '', ''
    piece_color, cell, slide = '', '', ''

    #iterate through every single cell on the chess board, determine moves available base on that cell
    for row in range (len(chess_board)):
        for column in range (len(chess_board[row])):
            cell = chess_board[row][column]
            if cell != ' ': # as long cell isnt empty determine all possible movements for piece in that cell
                piece = chess_board[row][column][0]
                print(piece)
                piece_color = piece_color(piece)
                slide = rays.get(piece)
                slide = slide[0]

                if turn_to_move == piece_color and piece.lower() != 'p': # if the piece's turn to move and it isnt a pawn, find poss. moves
                    for r in rays[piece.lower()]:     
                        done = False
                        step = 1
                        while not done: # accounts for sliding and staying in bounds of the board
                            target, done = movement_directions(cell, r, step) # finds target location & determines if movement is already outside 8x8
                            start_row = row
                            start_col = column
                            end_row = target[0]
                            end_col = target[1]
                            target_piece = chess_board[end_row][end_col] # finds piece at the end location for comparison
                            if target_piece == ' ': # move viable if empty square
                                move = basic_alg_notation_move(piece, start_row, start_col, end_row, end_col, capture)
                                possible_moves.append(move)
                            else:
                                target_piece_color = read_piece_color(target_piece)
                                if target_piece_color != player_color: # move viable if opponent_piece
                                    capture = 'x'
                                    move = basic_alg_notation_move(piece, start_row, start_col, end_row, end_col, capture)
                                    possible_moves.append(move)
                                else:
                                    done = True
                            if slide != 'slide': # if the piece doesnt slide end here, otherwise continue until unable
                                done = True
                            step += 1 
    return possible_moves

def pawn_movements(chess_board, row, column):
    """ generate possible pawn movements including en passant """
    possible_moves = []
    piece = 'p'
    start_row, start_col, end_row, end_col, capture = '', '', '', '', ''
    start_row = row
    start_col = column

    # one square movement
    if chess_board[row-1][column] == ' ': 
        end_row = row -1
        end_col = column
        possible_moves.append(basic_alg_notation_move(piece, start_row, start_col, end_row, end_col, capture))
        if row == 6 and chess_board[row-2][column] == ' ': # two square movement
            possible_moves.append(basic_alg_notation_move(piece, start_row, start_col, end_row, end_col, capture))




def basic_alg_notation_move(piece, start_row, start_column, end_row, end_column, capture): # tested and works
    """ basic long algebraic movement to add to moves list w/ only capture added """
    move = ''
    move = piece + get_rank_file(start_row, start_column) + capture + get_rank_file(end_row, end_column)
    return move

def alg_notation_move(piece, start_row, start_col, end_row, end_col, move_capture, move_promotion, move_check, move_checkmate):
    """ create the movement segment of a fen string
        converts to long algebraic notation - starting and ending destination
        normal: piece's uppercase letter, starting and ending coordinates
        capture: piece uppercase with 'x' before destination
        promotion: destination and then piece promoted to ex: e8Q <-- piece type not indicated bc pawn
        check: + at the end, double check (check by 2 enemies is ++) do i need that?
        checkmate: #
    """
    capture = ''
    if move_capture:
        capture = 'x'

    promotion = ''
    if move_promotion:
        promotion = 'Q'

    check = ''
    if move_check:
        check = '+'
    
    checkmate = ''
    if move_checkmate: # where does checkmate go in the fen string 
        checkmate = '#'

    return piece + get_rank_file(start_row, start_col) + capture + get_rank_file(end_row, end_col) + promotion + check + checkmate

# FUNCTIONS FOR CREATING NEW FEN STRINGS ---------------------------------------------------------------------------------------------------

def create_fen_board_setup():
    """create the board setup of a fenstring"""

    new_board_setup = ''
    return new_board_setup

def create_fen_castling():
    """ create the castling segment of a fen string"""
    if type == "K":
        castling_queen = ''
        castling_king = '0-0'
        return castling_queen, castling_king
    else:
        castling_queen = '0-0-0'
        castling_king = ''
        return castling_queen, castling_king

def create_fen_en_passant():
    """ create the en passant segment of a fen string"""
    new_en_passant = ''
    return new_en_passant

def create_halfmove():
    """ create the halfmove segment of a fen string """
    new_halfmove = 0
    return new_halfmove

def create_fullmove():
    """ create the fullmove segment of a fen string """
    new_fullmove = 0
    return new_fullmove

def create_entire_fen():
    """ add together all previous create_fen functions for entire fen string"""
    new_fen_string = ''

    return new_fen_string

starting_fen= "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
chess_board = create_filled_board(starting_fen)
turn_to_move = read_fen_turn_to_move(starting_fen)
#player_color, ai_color = fen_colors(starting_fen)
square = ''
#generate_moves(chess_board, square)

player_color, opponent_color = ' ',' '
player_color, opponent_color = read_fen_colors(starting_fen)



