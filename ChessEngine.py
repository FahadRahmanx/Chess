class ChessEngine:
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        self.moves = []
        self.whiteKingPos = (7,4)
        self.blackKingPos = (0,4)
        self.whiteTurn = True
        self.white_checkmate = False
        self.black_checkmate = False
        self.stalemate = False

        self.white_king_moved = False
        self.white_king_counter = 0
        self.black_king_moved = False
        self.black_king_counter = 0

        self.black_rook1_moved = False
        self.black_rook1_counter = 0
        self.black_rook1_pos = (0,0)

        self.black_rook2_moved = False
        self.black_rook2_counter = 0
        self.black_rook2_pos = (0,7)


        self.white_rook1_moved = False
        self.white_rook1_counter = 0
        self.white_rook1_pos = (7,0)


        self.white_rook2_moved = False
        self.white_rook2_counter = 0
        self.white_rook2_pos = (7,7)


        self.black_enPassant = False
        self.white_enPassant = False


    
    def white_left_castle_condition(self):
        if self.white_king_moved or self.white_rook1_moved:
            return False
        return True
    
    def white_right_castle_condition(self):
        if self.white_king_moved or self.white_rook2_moved:
            return False
        return True
    
    def black_left_castle_condition(self):
        if self.black_king_moved or self.black_rook1_moved:
            return False
        return True

    def black_right_castle_condition(self):
        if self.black_king_moved or self.black_rook2_moved:
            return False
        return True





class moves:

    pawn_white_start = [(6,i) for i in range(8)]
    pawn_black_start = [(1,i) for i in range(8)]



    def all_moves(self,r,c):
        white_pawn = [(r-1,c),(r-2,c),(r-1,c-1),(r-1,c+1)]
        black_pawn = [(r+1,c),(r+2,c), (r+1,c+1),(r+1,c-1)]
        knight = [(r+2,c+1),(r+2,c-1),(r-2,c+1),(r-2,c-1),(r+1,c+2),(r+1,c-2),(r-1,c+2),(r-1,c-2)]
        king = [(r,c-1),(r-1,c-1),(r+1,c-1),(r,c+1), (r+1,c+1),(r-1,c+1),(r+1,c),(r-1,c)]


        queen_u =[]
        queen_d =[]
        queen_l =[]
        queen_r =[]

        queen_ur =[]
        queen_ul =[]
        queen_dr =[]
        queen_dl =[]

        rook_u = []
        rook_d = []
        rook_l = []
        rook_r = []

        bishop_ur = []
        bishop_ul = []
        bishop_dr = []
        bishop_dl = []

        for i in range(8):
            move_1 = (r+i,c); move_2=(r,c+i); move_3=(r-i,c); move_4 = (r,c-i);move_5 = (r+i,c+i);move_6 = (r+i,c-i);move_7 = (r-i,c+i);move_8 = (r-i,c-i)
            queen_u.append(move_3)
            queen_d.append(move_1)
            queen_l.append(move_4)
            queen_r.append(move_2)
            queen_ur.append(move_7)
            queen_ul.append(move_8)
            queen_dr.append(move_5)
            queen_dl.append(move_6)

            rook_u.append(move_3)
            rook_d.append(move_1)
            rook_l.append(move_4)
            rook_r.append(move_2)

            bishop_ur.append(move_7)
            bishop_ul.append(move_8)
            bishop_dr.append(move_5)
            bishop_dl.append(move_6)

        queen = [queen_u,queen_d,queen_l,queen_r,queen_ul,queen_ur,queen_dl,queen_dr]
        rook = [rook_u,rook_d,rook_l,rook_r]
        bishop = [bishop_ul,bishop_ur, bishop_dl, bishop_dr]
        return [white_pawn,black_pawn,knight,bishop,rook,queen,king]
    

    # def canCastle(self,board,kingpos,castling):


    def valid_moves(self,r,c,moves,board, starting_pawn =False, king_pos = ()):
        if board[r][c] == "wP":
            valid = moves[0]
        elif board[r][c] == "bP":
            valid = moves[1]
        elif board[r][c][-1] == "N":
            valid = moves[2]
        elif board[r][c][-1] == "B":
            valid = moves[3]
        elif board[r][c][-1] == "R":
            valid = moves[4]
        elif board[r][c][-1] == "Q":
            valid = moves[5]
        elif board[r][c][-1] == "K":
            valid = moves[6]
        piece = board[r][c][-1]

        if piece == "P" or piece == "K" or piece == "N":
            i=0
            for move in valid:
                if move[0]<0 or move[0]>7 or move[1]>7 or move[1]<0:
                    valid[i] = (None,None)
                i+=1

        else:
            i=0
            for moves in valid:
                j=0
                for move in moves:
                    if move[0]<0 or move[0]>7 or move[1]>7 or move[1]<0:
                        valid[i][j] = (None,None)
                    j+=1
                i+=1
        turn = board[r][c][0]
        valid_n = []
        if piece == "K" or piece == "N":
            for row,col in valid:
                if row == None:
                    continue
                if board[row][col][0] != turn:
                    valid_n.append((row,col))

        if piece == "P":
            if board[r][c][0] == "w":
                for i,j in valid:
                    if i == None:
                        continue
                    if abs(r-i) == 1 and abs(c-j)==1:
                        if board[i][j][0] == "b":
                            valid_n.append((i,j))
                j = 1
                if starting_pawn:
                    j = 2
                for move in range(j):
                    i,j = valid[move]
                    if i == None:
                        continue
                    if board[i][j][0] == "b" or board[i][j][0] == "w"  :
                        break
                    else:
                        valid_n.append((i,j))

            elif board[r][c][0] == "b":
                for i,j in valid:
                    if i == None:
                        continue
                    if abs(r-i) == 1 and abs(c-j)==1:
                        if board[i][j][0] == "w":
                            valid_n.append((i,j))
                j = 1
                if starting_pawn:
                    j = 2
                for move in range(j):
                    i,j = valid[move]
                    if i == None:
                        continue
                    if board[i][j][0] == "b" or board[i][j][0] == "w"  :
                        break
                    else:
                        valid_n.append((i,j))
        if piece =="Q" or piece == "B" or piece == "R":
            for i in range(len(valid)):
                for j in range(len(valid[i])):
                    row = valid[i][j][0] #getting row and column from the tuple
                    col = valid[i][j][1]
                    if r == row and c == col :
                        continue
                    elif valid[i][j] == (None,None):
                        continue

                    elif board[row][col][0] == "w" and turn == "w":
                        break
                    elif board[row][col][0] == "w" and turn == "b":
                        valid_n.append(valid[i][j])
                        break
                    elif board[row][col][0] == "b" and turn == "b":
                        break
                    elif board[row][col][0] == "b" and turn == "w":
                        valid_n.append(valid[i][j])
                        break
                    else:
                        valid_n.append(valid[i][j])
        if len(king_pos) != 0:

            for i in range(len(valid_n)-1,-1,-1):
                new_row,new_col = valid_n[i]
                if r!=None and c!=None:
                    piece = board[r][c]

                    value = board[new_row][new_col]
                    board[new_row][new_col] = board[r][c]
                    board[r][c] = "--"
                    if piece == "wK" or piece == "bK":
                        if self.inCheck(board,(new_row,new_col)):
                            valid_n.remove(valid_n[i])
                        
                    elif self.inCheck(board,king_pos):

                        valid_n.remove(valid_n[i])
                    board[r][c] = board[new_row][new_col]
                    board[new_row][new_col] = value

        return valid_n

    def inCheck(self, board, king_pos, piece =""):      #king_pos in tuple


        r = king_pos[0]
        c = king_pos[1]
        turn = board[r][c][0]
        if piece !="":
            turn = piece
        if turn == "w":
            enemy = "b"
        else:
            enemy ="w"


        moves = self.all_moves(r,c)
        knight_check_moves = moves[2]
        all_other_moves = moves[5]
        #now removing out of bound moves
        i=0
        for moves in all_other_moves:
            j=0
            for move in moves:
                if move[0]<0 or move[0]>7 or move[1]>7 or move[1]<0:
                    all_other_moves[i][j] = (None,None)
                j+=1
            i+=1

        i=0
        for move in knight_check_moves:
            if move[0]<0 or move[0]>7 or move[1]>7 or move[1]<0:
                knight_check_moves[i] = (None,None)
            i+=1

        #checking for enemy pieces
        for i in range(len(knight_check_moves)):
            row = knight_check_moves[i][0]
            col = knight_check_moves[i][1]
            if row == r and col == c:
                continue
            elif knight_check_moves[i] == (None,None):
                continue
            elif board[row][col] == f"{enemy}N" :

                return True

                
        for i in range(len(all_other_moves)):
            for j in range(len(all_other_moves[i])):
                row = all_other_moves[i][j][0] #getting row and column from the tuple
                col = all_other_moves[i][j][1]
                if r == row and c == col :
                    continue
                elif all_other_moves[i][j] == (None,None):
                    continue

                elif board[row][col][0] == "w" and turn == "w":
                    break
                elif board[row][col][0] == "w" and turn == "b":
                    #this is enemy piece ,now check if this enemy piece can attack the king , for that generating all valid moves of this piece
                    all_enemy_moves = self.all_moves(row,col)
                    valid_enemy_moves = self.valid_moves(row,col,all_enemy_moves,board)
                    if (r,c) in valid_enemy_moves:
                        return True
                    break

                elif board[row][col][0] == "b" and turn == "b":
                    break
                elif board[row][col][0] == "b" and turn == "w":
                    #this is enemy piece ,now check if this enemy piece can attack the king , for that generating all valid moves of this piece
                    all_enemy_moves = self.all_moves(row,col)
                    valid_enemy_moves = self.valid_moves(row,col,all_enemy_moves,board)
                    if (r,c) in valid_enemy_moves:
                        return True
                    break
        return False




    def all_possible_valid_moves(self,board,turn,king_pos):
        Moves = []
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] !="--" and board[r][c][0] == turn:
                    all_enemy_moves = self.all_moves(r,c)
                    if board[r][c] == f"{turn}P":
                        if turn =="w":
                            if (r,c) in moves.pawn_white_start:
                                valid_enemy_moves = self.valid_moves(r,c,all_enemy_moves,board,True,king_pos)
                            else:
                                valid_enemy_moves = self.valid_moves(r,c,all_enemy_moves,board,False,king_pos)
                        elif turn =="b":
                            if (r,c) in moves.pawn_black_start:
                                valid_enemy_moves = self.valid_moves(r,c,all_enemy_moves,board,True,king_pos)
                            else:
                                valid_enemy_moves = self.valid_moves(r,c,all_enemy_moves,board,False,king_pos)

                    else:
                        valid_enemy_moves = self.valid_moves(r,c,all_enemy_moves,board,False,king_pos)
                    Moves.extend(valid_enemy_moves)
        return Moves


    def enPassant_move(self,board,start,end,piece):
        start_row,start_col = start
        new_row,new_col = end
        if piece == "wP" and new_row == start_row-2:
            if new_col+1<=7 and  board[new_row][new_col+1] == "bP":
                return True
            if new_col-1>=0 and board[new_row][new_col-1] == "bP":
                return True            
        if piece == "bP" and new_row == start_row+2:
            if new_col+1<=7 and  board[new_row][new_col+1] == "wP":
                return True
            if new_col-1>=0 and board[new_row][new_col-1] == "wP":
                return True
        return False

class pieces_moved:
    def __init__(self,start,end,board, castle_move = False, white_enPassent = False,black_enPassant = False):
        self.start_row = start[0]
        self.start_col = start[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_captured = board[self.end_row][self.end_col]
        self.castle_move = castle_move
        self.white_enPassant = white_enPassent
        self.black_enPassant = black_enPassant


