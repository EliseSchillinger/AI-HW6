# chess class (might use) --------------------------------------------------------
class game_state():
    """ keeps track of the overall state of the game and the board """
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.white_move = True
        self.moves_taken = []
        self.player_color = ''
        self.opponent_color = ''
        self.turn = ''
    

    def update_game_state(chess_board):
        pass

    def make_move(self, move):
        """ move piece from starting location to ending location """
        self.chess_board[move.start_row][move.start_column] = " "
        self.chess_board[move.end_row][move.end_column] = move.piece_moved
        self.moves_taken(move) #log the move so we can undo later
        self.my_move = not self.my_move # false once your move is done 

    def generate_moves(self):
        """ all possible moves regardless of check - except pawns """
        moves = []
        piece = ''
        square = ''
        # is there a better way to do this for every cell in a chess board
        for row in range (len(self.chess_board)):
            for column in range (len(self.chess_board[row])):
                square = self.chess_board[row][column]
                if square != '':
                    piece = self.chess_board[row][column][0]
                    #if ps turn to move and p != pawn <-- figure out that notation 
                        #for r in rays of piece:     idk what rays means in this context 
                            #done = False
                            #step = 1
                            #while not done:
                                #target = cell moves step num of squares in r direction from cell?
                                #if target out of bounds:
                                    #done = true
                                #else: 
                                    #piece = piece at location of target 
                                   # if piece == '':
                                        #move is square to target 
                                    #else:
                                    #if p' is opponent piece

                # if whites turn and their move, look at these pieces then look at all opposition piece moves for check

    def pawn_moves():
        """ all pawn movements"""
        pass                

                    

    def valid_moves(self):
        """ all valid movement: in other words not in check"""
        pass

    


class chess_move():
    """ converts between double list index and rank/file, keeps track of the chess pieces, 
        which pieces have been moved, which have been captured, move validity, etc 
    """
    # conversion between index and rank/file
    # key : value
    ranks_to_rows = { 0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1' }
    rows_to_ranks = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
    files_to_columns = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    columns_to_files = { 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

    #specifically for coordinate locations and piece movement
    def __init__(self, start, end, chess_board):
        self.start_row = start[0]
        self.start_column = start[1]
        self.end_row = end[0]
        self.end_column = end[1]
        self.piece_moved = chess_board[self.start_row][self.start_column]
        self.piece_captured = chess_board[self.end_row][self.end_column]

        #for notation purposes
        self.promotion = ''
        self.capture = ''
        self.piece_type = ''.upper()
        self.castle = False
        self.castling_king = ''
        self.castling_queen = ''
        self.check = ''

    def castling(self,type):
        """ determine the type of castling done and return for chess notation """
        self.castle = True
        if type == "K":
            self.castling_queen = ''
            self.castling_king = '0-0'
            return self.castling_queen, self.castling_king
        else:
           self.castling_queen = '0-0-0'
           self.castling_king = ''
           return self.castling_queen, self.castling_king

    def chess_notation(self, row, column):
        """ converts to long algebraic notation - starting and ending destination
            normal: piece's uppercase letter, starting and ending coordinates
            capture: piece uppercase with 'x' before destination
            promotion: destination and then piece promoted to ex: e8Q <-- piece type not indicated bc pawn
            check: + at the end, double check (check by 2 enemies is ++) do i need that?
            checkmate: #
        """
        # returns all relevant pieces of notation (if not applicable stays '')
        if not self.castling:
            return self.piece_type + self.get_rank_file(self.start_row, self.start_column) + self.capture + self.get_rank_file(self.end_row, self.end_column) + self.promotion + self.check
        else:
            if self.castling_king != '':
                return self.castling_king
            else:
                return self.castling_queen
    
    def get_rank_file(self, row, column):
        """ return the rank and file """
        return self.columns_to_files[column] + self.rows_to_ranks[row]
    def piece_promotion(self, row, column):
        """ use the location of the piece and add the promotion to that piece
            for now random promotion or always queen? 
        """

        pass 

# chess board creation and update functions ---------------------------------------------------------------------------
def copy_board(chess_board):
    """ copy board for new move generation """
    temp_board = []
    for i in range(len(chess_board)):
        temp_board.append(chess_board[i][:])
    return temp_board

def create_chess_board():
    """ returns an 'empty' 8x8 2d list ready to add chess pieces"""
    board = []
    for row in range(8):
        file = []
        for column in range(8):
            file.append(' ')
        board.append(file)
    return board

def create_filled_board(FEN):
    """ creates the chess gameboard based on a FEN string
        notes: chess indexing
            rows: 0-7 but in notation it is 8-1, reverse order of our index & w/o zero 
            columns: 0-7 but in notation a-h
        FEN: 
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

# FEN functions -------------------------------------------------------------------------------------------
def split_fen(my_FEN):
    """ split parts of the FEN into characters """
    return [char for char in my_FEN]

def fen_colors(self, FEN):
    """ determines the color of the AI player and opponent based on the FEN string """
    color_FEN = FEN.split(' ')
    color_FEN = color_FEN[1]

    if color_FEN == 'w':
        player_color = 'w'
        opponent_color = 'b'
    else:
        player_color = 'b'
        opponent_color = 'w'
    
    return player_color, opponent_color
    
def fen_castle(FEN, player_color):
    """ determines if Castling is possible for player or opponent based on the FEN string
        can be castling for one color, both, neither """
    castle_FEN = ''
    castle_FEN = FEN.split(' ')
    castle_FEN = castle_FEN[2]

    castle_options = []
    castle_options = split_fen(castle_FEN)

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

def fen_en_passant(FEN):
    """ determines if en passant is possible """
    player_en_passant = ' '
    player_en_passant = FEN.split(' ')
    player_en_passant = player_en_passant[3]
    
    return player_en_passant

def fen_halfmove(FEN):
    """ the number of halfmoves from the FEN string """
    halfmove = 0
    this_fen = ''
    this_fen = FEN.split(' ')
    halfmove = int(this_fen[4])

    return halfmove

def fen_fullmove(FEN):
    """ the number of fullmoves from the FEN string """
    fullmove = 0
    this_fen = ''
    this_fen = FEN.split(' ')
    fullmove = int(this_fen[5])
    return fullmove

def generate_fen():
    """ creates a FEN string based on the locations of the pieces on the board """
    pass

# other piece functions ----------------------------------------------------------------------------------
def player_pieces(chess_board, color):
    """ determines all the pieces a player has on the board through iteration """
    pieces = []
    pass
