# FUNCTIONS FOR CREATING AND COPYING THE CHESS BOARD ------------------------------------------------------------------------------------------
import turtle


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

def read_fen_player_pieces(FEN):
    """ retrieve all player pieces based on color and given fen string """
    player_pieces = []
    current_FEN = FEN.split(' ')
    current_FEN = current_FEN[0].split('/') #take only piece location segment of FEN
    current_FEN = current_FEN[-1] # want end pieces bc those are the player pieces (think about board orientation and printing)
    player_pieces = split_FEN(current_FEN)
    
    return player_pieces


starting_fen= "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
player_color = 'w'
thees = read_fen_player_pieces(starting_fen, player_color)
print(thees)

def read_fen_colors(FEN):
    """ determines the color of the AI player and opponent based on the FEN string
    """
    current_FEN = FEN.split(' ')
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


# RANK-FILE TRANSLATION -----------------------------------------------------------------------------------------------------------------

# swapping between 2D list index and rank/file
# maybe just add these into the functions
rows_to_ranks = { 0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1' }
ranks_to_rows = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
files_to_columns = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
columns_to_files = { 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

def get_rank_file(row, column):
    """ return the rank and file from the 2D list index """
    return columns_to_files[column] + rows_to_ranks[row]

def revert_2D_index(move):
        return columns_to_files[move[0]], rows_to_ranks[move[1]], columns_to_files[move[2]], rows_to_ranks[move[3]]

def revert_rank_to_row_end(move):
    """ revert from rank and file back to 2D list indexing - only ending location """
    # alter if necessary
    if len(move) == 4:
        return [ranks_to_rows[move[-1]], files_to_columns[move[-2]]]
    elif len(move) == 5:
        return [ranks_to_rows[move[-2]], files_to_columns[move[-3]]]


# ----------------------------------------------- tested and works above ------------------------------------------------------------------

# PIECE MOVEMENT, LOGIC, AND LOCATION FUNCTIONS -------------------------------------------------------------------------------------------
def find_player_piece(piece, chess_board, player_color):
    """ find locations of a specific player piece 
        function created just in case
    """
    piece_locations = []
    this_piece = ''
    for row in range(len(chess_board)):
        for column in range (len(chess_board[row])):
            this_piece = chess_board[row][column]
            if player_color == read_piece_color(this_piece):
                if piece == this_piece:
                    piece_locations.append([row, column])
    return piece_locations


def find_player_pieces(chess_board, player_color):
    """ find all pieces of one color left on the board
        technically can be used for opponent pieces also 
    """
    all_pieces = []
    this_piece = ''
    # iterate through entire board, test each cell to see if it's a player piece and track its location 
    for row in range(len(chess_board)):
        for column in range (len(chess_board[row])):
            this_piece = chess_board[row][column]
            if player_color == read_piece_color(this_piece):
                all_pieces.append([row, column])
    return all_pieces

def find_kings(chess_board, player_color):
    """ find king locations on the board """
    player_king_loc, opponent_king_loc = [],[]
    this_king = ''
    this_king_loc = []

    # iterate over the board to find the kings
    for row in range(len(chess_board)):
        for column in range(len(chess_board)):
            if chess_board[row][column].lower() == 'k':
                this_king = chess_board[row][column]
                this_king_loc = [row, column]
                if player_color == read_piece_color(this_king): # if same color as player, track location
                    player_king_loc = this_king_loc
                else:
                    opponent_king_loc = this_king_loc # track opponent king location 
    return player_king_loc, opponent_king_loc

def movement_directions (cell, r, step): 
    """ movement through the 2d list using cardinal directions as indicators - alterations for knight movement """
    next_location = cell[:]
    out_of_bounds = False

    # could i replace w another dictionary that has the direction and the way it alters row/column 
    # to get rid of all if statements and clean up?

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
            
        # if piece out of board bounds, o_o_b becomes true - does not add to move list
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

def generate_moves(chess_board, turn_to_move, player_color):
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
                piece_color = read_piece_color(piece)
                slide = rays.get(piece)
                slide = slide[0]
                if turn_to_move == piece_color and piece.lower() != 'p': # if the piece's turn to move and it isnt a pawn, find poss. moves
                    for r in rays[piece.lower()]:     
                        done = False
                        step = 1
                        while not done: # accounts for sliding and staying in bounds of the board
                            target, done = movement_directions(cell, r, step) # finds target location & determines if movement already outside 8x8
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
                            if slide != 'slide': # if the piece doesnt slide, end here, otherwise continue until unable
                                done = True
                            step += 1 
    return possible_moves
def generate_piece_moves(chess_board, player_color, piece, rays):
    """ generate movements for a specific piece """
    piece_moves = []
    for p in rays:
        if piece == p:
            # generate all movements for that piece
            # if king account for castling, check, being threatened etc
            # doesnt work for pawns. similar logic to above?
            pass
        pass
    return piece_moves

def generate_pawn_movements(chess_board, row, column, player_color):
    """ generate possible pawn movements including en passant """

    # i think this is applicable for both black and white bc if you start as black (or the ai plays against itself) you're always on the bottom?
    possible_pawn_moves = []
    move = ''
    promotions = ['n','r','b','q']
    piece = 'p'
    start_row, start_col, end_row, end_col, this_piece, capture = '', '', '', '', '', ''
    start_row = row
    start_col = column

    # one square movement
    if chess_board[row-1][column] == ' ': 
        end_row = row -1
        end_col = column
        move = basic_alg_notation_move(piece, start_row, start_col, end_row-1, end_col, capture)
        possible_pawn_moves.append(move)
        if row + 1 == 0: # promotion
            for p in promotions:
                possible_pawn_moves.append(move+p)
        # two square movement
        if row == 6 and chess_board[row-2][column] == ' ': 
            possible_pawn_moves.append(basic_alg_notation_move(piece, start_row, start_col, end_row-2, end_col, capture))
    # left capture
    if column -1 >= 0: # like in movement_directions, keep in bounds
        this_piece = chess_board[row-1][column-1]
        piece_color = read_piece_color(this_piece)
        if player_color != piece_color:
            capture = 'x'
            move = basic_alg_notation_move(this_piece, start_row, start_col, end_row-1, end_col-1, capture)
            possible_pawn_moves.append(move)
        if row + 1 == 0: # promotion
            for p in promotions:
                possible_pawn_moves.append(move+p)
    # right capture
    if column + 1 <= 7:
        this_piece = chess_board[row-1][column+1]
        piece_color = read_piece_color(this_piece)
        capture = 'x'
        move = basic_alg_notation_move(this_piece, start_row, start_col, end_row-1, end_col-1, capture)
        possible_pawn_moves.append(move)
        if row + 1 == 0: # promotion
            for p in promotions:
                possible_pawn_moves.append(move+p)
    return possible_pawn_moves

def check(chess_board, player_color, turn_to_move):
    """ creating check for kings - track the king, view surrounding pieces """
    # find the king on the board
    player_king, opponent_king = [], []
    player_king, opponent_king = find_kings(chess_board, player_color)

    player_king_check = False
    opponent_king_check = False

    #check every single piece
    possible_moves = generate_moves(chess_board, turn_to_move, player_color)
    for move in possible_moves:
        if opponent_king == revert_rank_to_row_end(move): # if the opponent king is in the same location as the ending pos. of the move
            opponent_king_check = True
            return player_king_check, opponent_king_check
        elif player_king == revert_rank_to_row_end(move): # ^ same logic but with player king
            player_king_check = True
            return player_king_check, opponent_king_check
    return player_king_check, opponent_king_check
            
def generate_valid_moves(chess_board, player_color, turn_to_move, possible_moves):
    """ find all the valid movements """
    checkmate, stalemate, player_king_check, opponent_king_check = False, False, False, False
    for move in range(len(possible_moves)-1, -1, -1): # reverse so index isnt impacted
        player_king_check, opponent_king_check = check(chess_board, player_color, turn_to_move)
        if player_king_check:
            possible_moves.remove(move)
    if len(possible_moves) == 0:
        if player_king_check:
            checkmate = True
        else:
            stalemate = True
    return possible_moves, checkmate, stalemate

def castling(chess_board, turn_to_move, player_color):
    """ set up castling with kings: move king 2 squares and rook goes on opp side
        3 squares between rook and king must be empty 
        king not in check
        squares cannot be "under attack"
    """
    # basically first move by king or rook 
    pass

# FUNCTIONS FOR CREATING NEW FEN STRINGS ---------------------------------------------------------------------------------------------------

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

def create_castling_notation():
    """ create the castling segment for piece locations of fen string """
    if type == "K":
        castling_queen = ''
        castling_king = '0-0'
        return castling_queen, castling_king
    else:
        castling_queen = '0-0-0'
        castling_king = ''
        return castling_queen, castling_king

def create_fen_board_setup(prev_chess_board):
    """create the board setup of a fenstring """
    updated_chess_board = []
    updated_chess_board = copy_board(prev_chess_board)

    return updated_chess_board

def create_entire_fen(chosen_move, prev_chess_board, previous_fen):
    """ add together all previous create_fen functions for entire fen string """
    player_color, opponent_color, player_castle, player_color, en_passant = '', '', '','', ''
    halfmove, fullmove = 0, 0
    new_fen_string = ''
    updated_chess_board = []
    # player/opponent color
    player_color, opponent_color = read_fen_colors(previous_fen)
    # previous turn
    prev_turn_to_move = read_fen_turn_to_move(previous_fen)
    # previous castling
    player_castle, opponent_castle = read_fen_castle(player_color, previous_fen)
    # piece placement
    print(chosen_move) # includes starting and ending positions

    start_column, start_row, end_column, end_row = revert_2D_index(chosen_move)
    piece_moved = prev_chess_board[start_row][start_column].lower()
    if piece_moved == 'p':
        #en passant
        pass
    elif piece_moved == 'r':
        #castling
        if prev_turn_to_move == 'w':
            if player_color == 'w':
                if 'Q' in player_castle:
                    player_castle.remove('Q')
                elif 'K' in player_castle:
                    player_castle.remove('K')
            #continue thought process w/ castling. needsto be according to movement of pieces
                


    # turn to move
    if prev_turn_to_move == 'w':
        turn_to_move = 'b'
    else:
        turn_to_move = 'w'
    #castling
    """ if the king or rook move from row 7 or spaces between arent empty
            depending on color
                remove king or queenside castling availability
        add black and white castling to string for FEN
    """
    # en passant
    en_passant = '-'
    # halfmove
    halfmove = read_fen_halfmove(previous_fen) + 1
    # fullmove
    fullmove = read_fen_fullmove(previous_fen)

    updated_chess_board = copy_board(prev_chess_board)
    updated_chess_board[end_row][end_column] = prev_chess_board[start_row][start_column] # update cell w/ the piece movement
    updated_chess_board[start_row][start_column] = ' ' # clear cell
    
    #create piece location section from updated board
    empty_space = 0
    piece_fen = ''

    # look for empty space in the board for piece location set up of fen string - keep testing
    """
    for row in updated_chess_board:
        for col in row:
            if col == ' ':
                empty_space += 1 
            else:
                if empty_space != 0:
                    piece_fen += str(empty_space)
                piece_fen += col
                empty_space = 0 
        if empty_space != 0:
            piece_fen += str(empty_space)
            empty_space = 0
        piece_fen += '/'
        """
    space = ' '
    castling = player_castle + opponent_castle
    new_fen_string = piece_fen + space + turn_to_move + space + castling + space + en_passant + space + str(halfmove) + space + str(fullmove)

    return new_fen_string, updated_chess_board

# since my code doesn't totally work im just trying to show that I understand what the algorithm would do
def term(fen_string, chess_board, last_8_moves, turn_to_move, player_color):
    """ tells us if state is terminal: aka checkmate, stalemate, our draw rule """
    valid_moves = []
    possible_moves = []
    possible_moves = generate_moves(chess_board,turn_to_move, player_color)
    valid_moves = generate_valid_moves(chess_board, player_color, turn_to_move, possible_moves)

    # if terminal, return true and the empty moves list. otherwise false and actual valid movements
    if len(valid_moves) == 0: #terminal: checkmate or stalemate
        return True, valid_moves
    if int(read_fen_halfmove(fen_string)) >= 99:
        valid_moves = []
        return True, valid_moves
    # draw rule from assignment doc - can i shorten?
    if last_8_moves[0] == last_8_moves[4] and last_8_moves[1] == last_8_moves[5] and last_8_moves[2] == last_8_moves[6] and last_8_moves[3] == last_8_moves[7]: 
        valid_moves = []
        return True, valid_moves
    return False, valid_moves

def heuristic(fen_string): 
    """ create heuristic based on standard valuations assigned to different pieces
        use example from class
    """
    total = 0
    piece_values = {'p':1, 'n':3, 'b':3, 'r':5, 'q':9, 'k':100 }
    piece_locations = []
    piece_locations = read_fen_player_pieces(fen_string)
    # iterate through player piece list, accumulate total based on value assigned to piece in dict. 
    for piece in piece_locations:
        total += piece_values[piece.lower()]
    return total


def utility(fen_string, chess_board, player_color, valid_moves, turn_to_move, last_8_moves):
    """ tells us the utility of terminal states: returns a value """
    rays = {'k':  ['n','ne', 'e', 'se', 's', 'sw','w', 'nw']}
    term_val = 0
    # starting with king = 100
    piece, player_king, opponent_king = '','', ''
    player_king, opponent_king = find_kings(chess_board, player_color)

    if player_color == 'w':
        piece = 'K'
    else:
        piece = 'k'

    possible_king_moves = generate_piece_moves(chess_board, player_color,piece, rays)
    # if i created a function to individually find movements for specific pieces it would be this: would return is_king_threatened
    is_king_threatened = False
    
    # just like in term function: draw rules
    if last_8_moves[0] == last_8_moves[4] and last_8_moves[1] == last_8_moves[5] and last_8_moves[2] == last_8_moves[6] and last_8_moves[3] == last_8_moves[7]: 
        term_val = 0
        return term_val
    #use a function to determine threat levels and impact score - boolean
    if len(possible_king_moves) == 0:
        if len(valid_moves) == 0: # no moves left anywhere: stalemate
            term_val = 0
            return term_val
        if(is_king_threatened): # checkmate for player or opponent
            if turn_to_move == player_color: 
                term_val = -100
                return term_val
            else:
                term_val = 100
                return term_val
    return term_val

def max_choice(fen_string, depth, prev_moves):
    """ tries to find the best action - maximizes min_value( result(s0,action))
        look at class notes - follow general structure 
    """
    player_color, opponent_color = read_fen_colors(fen_string)
    turn_to_move = read_fen_turn_to_move(fen_string)
    chess_board = create_chess_board()
    chess_board = create_filled_board(fen_string)
    possible_moves = generate_moves(chess_board, turn_to_move, player_color)
    valid_moves = generate_valid_moves(chess_board, player_color, turn_to_move, possible_moves)

    score, best_score = 0, 0
    best_move = []

    # for each move, execute the move and use the new fen and chess board to do min_val
    for move in valid_moves:
        prev_moves.append(move)
        new_fen = create_entire_fen(move, chess_board, fen_string)
        updated_chess_board = create_chess_board()
        updated_chess_board = create_filled_board(new_fen)
        
        score = min_val(updated_chess_board, new_fen, player_color,turn_to_move, depth, prev_moves) # recursive min
        if score > best_score:
            best_move = move
            best_score = score
        prev_moves.pop() # removes last move from list to try next move
    return best_move

def min_val(chess_board, fen_string, player_color, turn_to_move, depth, prev_moves):
    """ tries to find the state w/ minimum value """
    terminal = False
    valid_moves = []
    # check first:
    terminal, valid_moves = term(fen_string, chess_board, prev_moves, turn_to_move, player_color)
    # return values if true: depth limit hit/ score of term state
    if depth == 0:
        state_heur = heuristic(fen_string)
        return state_heur
    if terminal:
        state_util = utility(fen_string, chess_board, player_color, valid_moves, turn_to_move, prev_moves)
        return state_util 
    
    score, best_score = 0,0
    # test new move, create new fen and board, minimize the max score
    for move in valid_moves:
        prev_moves.append(move)
        new_fen = create_entire_fen(move, chess_board, fen_string)
        updated_chess_board = create_chess_board()
        updated_chess_board = create_filled_board(new_fen)
        score = max_val(new_fen, updated_chess_board, player_color, turn_to_move, valid_moves, prev_moves, depth-1)
        # return the best score
        if score < best_score:
            best_score = score
    return best_score

def max_val(fen_string, chess_board, player_color, turn_to_move, valid_moves, prev_moves, depth):
    """ tries to find state w/ max value
        extremely similar to min_val set up
    """
    terminal = False
    valid_moves = []
    # check first:
    terminal, valid_moves = term(fen_string, chess_board, prev_moves, turn_to_move, player_color)
    # return values if true: depth limit hit/ score of term state
    if depth == 0:
        state_heur = heuristic(fen_string)
        return state_heur
    if terminal:
        state_util = utility(fen_string, chess_board, player_color, valid_moves, turn_to_move, prev_moves)
        return state_util 
    
    score, best_score = 0,0
    # test new move, create new fen and board, minimize the max score
    for move in valid_moves:
        prev_moves.append(move)
        new_fen = create_entire_fen(move, chess_board, fen_string)
        updated_chess_board = create_chess_board()
        updated_chess_board = create_filled_board(new_fen)
        score = min_val(new_fen, updated_chess_board, player_color, turn_to_move, valid_moves, prev_moves, depth-1)
        # return the best score
        if score > best_score:
            best_score = score
        prev_moves.pop()
    return best_score