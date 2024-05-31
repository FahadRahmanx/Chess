import pygame
import ChessEngine as chess
import sys
from pygame.locals import *
from tkinter import messagebox
import promotion
import pygame.gfxdraw

pygame.init()
check_sq = ()

dimension = 8
display_size = 512
sq_size = display_size//(dimension)

screen = pygame.display.set_mode((display_size,display_size),0,32)
engine = chess.ChessEngine()
board = engine.board

sq_selected = ()

HIGHLIGHT_COLOR = (242,202,92)
HIGHLIGHT_COLOR_VALID = (242,202,92,100)
last_move_color = (242, 97, 63,40)

pygame.display.set_caption("CHESS (PvP)")
images = {}
def loadImages():
    pieces = ["wR","wB","wN","wK","wQ","wP","bR","bB","bN","bK","bQ","bP"]
    for piece in pieces:
        loaded_img = pygame.image.load(f"images/{piece}.png")
        images[piece] = pygame.transform.scale(loaded_img,(sq_size,sq_size))
highlight_sq = []
valid_move = []


#light red (255,0,0,160)  light dark (81,37,34,160) light orange (255, 175, 66,120)
def drawboard():
    light_brown = (185,156,107)
    skin_brown = (213,196,161)
    red = (255,0,0,100)
    colour = [skin_brown,light_brown]
    for r in range(dimension):
        for c in range(dimension):
            color = colour[(r+c)%2]
            pygame.draw.rect(screen,color,(c*sq_size,r*sq_size,sq_size,sq_size))
            if (r,c) in highlight_sq :
                pygame.draw.rect(screen,HIGHLIGHT_COLOR,(c*sq_size,r*sq_size,sq_size,sq_size))
            # if (r,c) in check_sq:
            #     pygame.draw.rect(screen,red,(c*sq_size,r*sq_size,sq_size,sq_size))

    highlight_surface = pygame.Surface((sq_size, sq_size), pygame.SRCALPHA)
    highlight_surface.fill(HIGHLIGHT_COLOR_VALID)

    highlight_surface2 = pygame.Surface((sq_size, sq_size), pygame.SRCALPHA)
    highlight_surface2.fill(red)
    highlight_surface3 = pygame.Surface((sq_size, sq_size), pygame.SRCALPHA)
    highlight_surface3.fill(last_move_color)
    # Draw the highlighted squares
    for (row, col) in valid_move:
        screen.blit(highlight_surface, (col * sq_size, row * sq_size))
    if len(check_sq) == 2:
        row, col = check_sq
        screen.blit(highlight_surface2, (col * sq_size, row * sq_size))
    if len(engine.moves) != 0:
        MOVE = engine.moves[-1]
        start_r,start_c = MOVE.start_row,MOVE.start_col
        end_r ,end_c = MOVE.end_row,MOVE.end_col
        screen.blit(highlight_surface3, (start_c * sq_size, start_r * sq_size))
        screen.blit(highlight_surface3, (end_c * sq_size, end_r * sq_size))


    
def drawPieces():

    for r in range(dimension):
        for c in range(dimension):
            if board[r][c]!="--":
                piece = board[r][c]
                screen.blit(images[piece], Rect(c*sq_size,r*sq_size,sq_size,sq_size))



count = 0
counts = [0]
def pop_n_times(ar, n):
    for i in range(n):
        ar.pop()
    return
white_turn = engine.whiteTurn

special_move = []
white_enPassant = []
special_pawn = []
black_enPassant = []
drawboard()
loadImages()
drawPieces()
pawn_white_start = [(6,i) for i in range(8)]
pawn_black_start = [(1,i) for i in range(8)]
current_move = []
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            position = [position[0]//sq_size,position[1]//sq_size]      #present in [y,x] not [x,y]
            y,x = position
            current_move.append(position)

            if board[x][y] != "--" and len(current_move)==1:
                if (x,y) not in highlight_sq:
                    highlight_sq.append((x,y))

                else:
                    highlight_sq = []
                piece = board[current_move[0][1]][current_move[0][0]][0]
                if piece == "w": 
                    enemy = "b"
                else:
                    enemy = "w"
                piece_name = board[current_move[0][1]][current_move[0][0]]
                type = piece_name[1]
                if piece == "w" and white_turn or piece == "b" and not white_turn:

                    list_all_moves = chess.moves().all_moves(current_move[0][1],current_move[0][0])
                    if (current_move[0][1],current_move[0][0]) in pawn_white_start and piece_name == "wP":
                        valid = chess.moves().valid_moves(current_move[0][1],current_move[0][0],list_all_moves,board,True,engine.whiteKingPos)

                    elif (current_move[0][1],current_move[0][0]) in pawn_black_start and piece_name == "bP":
                        valid = chess.moves().valid_moves(current_move[0][1],current_move[0][0],list_all_moves,board,True,engine.blackKingPos)
                    else:
                        if piece == "w":
                            valid = chess.moves().valid_moves(current_move[0][1],current_move[0][0],list_all_moves,board,False,engine.whiteKingPos)
                        else:
                            valid = chess.moves().valid_moves(current_move[0][1],current_move[0][0],list_all_moves,board,False,engine.blackKingPos)
                    
                    # Rules for castling when king is in check it cant castle
                    # match Castling conditions
                    #check first if the piece is king
                    #check if the king and rook has been moved previously
                    #check on two places that king doesnt get a check and no piece in between
                
                    r,c = current_move[0][1],current_move[0][0]
                    if piece == "w":
                        can_castle_left = engine.white_left_castle_condition()
                        can_castle_right = engine.white_right_castle_condition()

                    else:
                        can_castle_left = engine.black_left_castle_condition()
                        can_castle_right = engine.black_right_castle_condition()

                    if (board[r][c][1] == "K"  and can_castle_right):
                        #check right rook and see there is nothing in between them
                        if board[r][c+1] == "--" and board[r][c+2] == "--":
                            #check that the right 3 positions arent targetted by enemy
                            if piece == "w":
                                if not chess.moves().inCheck(board,(r,c),"w") and not chess.moves().inCheck(board,(r,c+1),"w") and not chess.moves().inCheck(board,(r,c+2),"w"):
                                    special_move.append((r,c+2))
                            if piece == "b":
                                if not chess.moves().inCheck(board,(r,c),"b") and not chess.moves().inCheck(board,(r,c+1),"b") and not chess.moves().inCheck(board,(r,c+2),"b"):
                                    special_move.append((r,c+2))

                    
                    if (board[r][c][1] == "K"  and can_castle_left):
                        #check left rook and see there is nothing in between them
                        if board[r][c-1] == "--" and board[r][c-2] == "--" and board[r][c-3] == "--":
                            #check that the right 3 positions arent targetted by enemy
                            if piece == "w":
                                if not chess.moves().inCheck(board,(r,c),"w") and not chess.moves().inCheck(board,(r,c-1),"w") and not chess.moves().inCheck(board,(r,c-2),"w"):
                                    special_move.append((r,c-2))
                            if piece == "b":
                                if not chess.moves().inCheck(board,(r,c),"b") and not chess.moves().inCheck(board,(r,c-1),"b") and not chess.moves().inCheck(board,(r,c-2),"b"):
                                    special_move.append((r,c-2))

                    #en passent working here 
                    #if king gets in check after en passant then thats not valid move


                    if board[r][c] == "wP" and engine.white_enPassant:
                        if len(white_enPassant)>2:
                            d = []
                            a = white_enPassant[-2]
                            b = white_enPassant[-1]
                            d.append(a)
                            d.append(b)
                            white_enPassant = d

                        count = counts[-1]
                        if count>0 and engine.white_enPassant and white_enPassant == []:
                            move = engine.moves[-1]
                            # # if pawn bP and end_col+1 == bp move (end_row+1,end_col),(end_row,end_col+1)
                            # if move.piece_moved == "bP" and board[move.end_row][move.end_col+1] == "bP":

                                                                        
                            if move.piece_moved == "bP" and move.end_row == move.start_row+2: 
                                if move.end_col+1<=7 and  board[move.end_row][move.end_col+1] == "wP":
                                    white_enPassant.append([(move.end_row-1,move.end_col),(move.end_row,move.end_col+1)])
                                if move.end_col-1>=0 and board[move.end_row][move.end_col-1] == "wP":
                                    white_enPassant.append([(move.end_row-1,move.end_col),(move.end_row,move.end_col-1)])


                        if len(white_enPassant) ==2 or len(white_enPassant) ==1 and count >=1:
                            enPassant = white_enPassant[-1]
                            valid_loc = enPassant[0]
                            pawn_loc = enPassant[1]
                            if (r,c) == pawn_loc:
                                board[valid_loc[0]][valid_loc[1]] = board[pawn_loc[0]][pawn_loc[1]]
                                board[pawn_loc[0]][pawn_loc[1]] = "--"
                                board[valid_loc[0]+1][valid_loc[1]] = "--"
                                if not chess.moves().inCheck(board,engine.whiteKingPos):
                                    special_pawn.append(valid_loc)
                                board[valid_loc[0]][valid_loc[1]] = "--"
                                board[pawn_loc[0]][pawn_loc[1]] = "wP"
                                board[valid_loc[0]+1][valid_loc[1]] = "bP"
                        
                        if len(white_enPassant) ==2 and count ==2:

                            enPassant = white_enPassant[-2]
                            valid_loc = enPassant[0]
                            pawn_loc = enPassant[1]
                            if (r,c) == pawn_loc:
                                board[valid_loc[0]][valid_loc[1]] = board[pawn_loc[0]][pawn_loc[1]]
                                board[pawn_loc[0]][pawn_loc[1]] = "--"
                                board[valid_loc[0]+1][valid_loc[1]] = "--"
                                if not chess.moves().inCheck(board,engine.whiteKingPos):
                                    special_pawn.append(valid_loc)
                                board[valid_loc[0]][valid_loc[1]] = "--"
                                board[pawn_loc[0]][pawn_loc[1]] = "wP"
                                board[valid_loc[0]+1][valid_loc[1]] = "bP"




                    if board[r][c] == "bP" and engine.black_enPassant:
                        if count>0 and engine.black_enPassant and black_enPassant == []:
                            move = engine.moves[-1]
                            if move.piece_moved == "wP" and move.end_row == move.start_row-2:
                                if move.end_col+1<=7 and  board[move.end_row][move.end_col+1] == "bP":
                                    black_enPassant.append([(move.end_row+1,move.end_col),(move.end_row,move.end_col+1)])
                                if move.end_col+1<=7 and  board[move.end_row][move.end_col-1] == "bP":
                                    black_enPassant.append([(move.end_row+1,move.end_col),(move.end_row,move.end_col-1)])
                        if len(black_enPassant)>2:
                            d = []
                            a = black_enPassant[-2]
                            b = black_enPassant[-1]
                            d.append(a)
                            d.append(b)
                            black_enPassant = d
                        count = counts[-1]

                        if len(black_enPassant) ==2 or len(black_enPassant) ==1 and count >=1:
                            enPassant = black_enPassant[-1]
                            valid_loc = enPassant[0]
                            pawn_loc = enPassant[1]
                            if (r,c) == pawn_loc:
                                board[valid_loc[0]][valid_loc[1]] = board[pawn_loc[0]][pawn_loc[1]]
                                board[pawn_loc[0]][pawn_loc[1]] = "--"
                                board[valid_loc[0]-1][valid_loc[1]] = "--"
                                if not chess.moves().inCheck(board,engine.blackKingPos):
                                    special_pawn.append(valid_loc)
                                board[valid_loc[0]][valid_loc[1]] = "--"
                                board[pawn_loc[0]][pawn_loc[1]] = "bP"
                                board[valid_loc[0]-1][valid_loc[1]] = "wP"
                        if len(black_enPassant) ==2 and count ==2:
                            enPassant = black_enPassant[-2]
                            valid_loc = enPassant[0]
                            pawn_loc = enPassant[1]
                            if (r,c) == pawn_loc:
                                board[valid_loc[0]][valid_loc[1]] = board[pawn_loc[0]][pawn_loc[1]]
                                board[pawn_loc[0]][pawn_loc[1]] = "--"
                                board[valid_loc[0]-1][valid_loc[1]] = "--"
                                if not chess.moves().inCheck(board,engine.blackKingPos):
                                    special_pawn.append(valid_loc)
                                board[valid_loc[0]][valid_loc[1]] = "--"
                                board[pawn_loc[0]][pawn_loc[1]] = "bP"
                                board[valid_loc[0]-1][valid_loc[1]] = "wP"                        

                    valid_move.extend(valid)
                    valid_move.extend(special_move)
                    valid_move.extend(special_pawn)

             
            if board[current_move[0][1]][current_move[0][0]] == '--':
                current_move = []
                highlight_sq = []
                valid_move = []
                special_move = []
                special_pawn = []

            elif len(current_move) == 2 and current_move[0] == current_move[1]:
                current_move = []
                highlight_sq = []
                valid_move = []
                special_move = []
                special_pawn = []
            elif len(current_move) == 2 and current_move[0] != current_move[1]:
                start_row = current_move[0][1]
                start_col = current_move[0][0]

                new_row = current_move[1][1]
                new_col = current_move[1][0]

                if (new_row,new_col) in valid_move or (new_row,new_col) in special_move or (new_row,new_col) in special_pawn:

                    engine.black_enPassant = False
                    engine.white_enPassant = False

                    start = (current_move[0][1],current_move[0][0])
                    end = (current_move[1][1],current_move[1][0])
                    #en passant move
                    if (new_row,new_col) in special_pawn:

                        turn = board[start_row][start_col][0]
                        if turn  == "w":
                            engine.moves.append(chess.pieces_moved(start,end,board,False,True))

                            board[new_row][new_col] = board[start_row][start_col]
                            board[start_row][start_col] = "--"
                            board[new_row+1][new_col] = "--"
                        if turn == "b":
                            engine.moves.append(chess.pieces_moved(start,end,board,False,False,True))

                            board[new_row][new_col] = board[start_row][start_col]
                            board[start_row][start_col] = "--"
                            board[new_row-1][new_col] = "--"
                        white_turn = not white_turn
                    #castling
                    elif (new_row,new_col) in special_move:
                        engine.moves.append(chess.pieces_moved(start,end,board,True))
                        if new_col == 2:
                            board[new_row][new_col] = board[start_row][start_col]
                            board[start_row][start_col] = "--"

                            board[new_row][3] = board[new_row][0]
                            board[new_row][0] = "--"


                        if new_col == 6:
                            board[new_row][new_col] = board[start_row][start_col]
                            board[start_row][start_col] = "--"

                            board[new_row][5] = board[new_row][7]
                            board[new_row][7] = "--"                

                        white_turn = not white_turn


                    else:
                        engine.moves.append(chess.pieces_moved(start,end,board))
                        turn  = board[start_row][start_col][0]
                        #en passant conditions
                        #if white moves pawn 2 places up the -2 on rows
                        #then first en passant condition satisfied
                        #check if on  right or left of this pawn there is enemy pawn 
                        #if enemy pawn then that enemy pawn has the ability to capture that pawn by moving to col of white and +1 row ==> special move added

                            
                        if board[start_row][start_col] == "wP" and new_row == start_row-2:
                            count = 0
                            if new_col+1<=7 and  board[new_row][new_col+1] == "bP":
                                engine.black_enPassant = True
                                black_enPassant.append([(new_row+1,new_col),(new_row,new_col+1)]) # if pawn bP and end_col+1 == bp move (end_row+1,end_col),(end_row,end_col+1)
                                count +=1

                                #first(r,c) give the location that enemy pawn will take , second(r,c) will give the location of enemy pawn which can do en passant
                                
                            if new_col-1>=0 and board[new_row][new_col-1] == "bP":
                                count+=1
                                engine.black_enPassant = True
                                black_enPassant.append([(new_row+1,new_col),(new_row,new_col-1)])                                

                        if board[start_row][start_col][1] == "P" and turn =="b" and new_row == start_row+2: 
                            count = 0

                            if new_col+1<=7 and  board[new_row][new_col+1] == "wP":
                                count+=1

                                engine.white_enPassant = True
                                white_enPassant.append([(new_row-1,new_col),(new_row,new_col+1)])
                                
                            if new_col-1>=0 and board[new_row][new_col-1] == "wP":
                                count+=1
                                engine.white_enPassant = True
                                white_enPassant.append([(new_row-1,new_col),(new_row,new_col-1)])      
                        capture_piece = board[current_move[1][1]][current_move[1][0]]
                        board[current_move[1][1]][current_move[1][0]] = board[current_move[0][1]][current_move[0][0]]
                        if board[current_move[1][1]][current_move[1][0]] == "wP" or board[current_move[1][1]][current_move[1][0]] == "bP":
                            if current_move[1][1] == 7 or current_move[1][1] == 0:
                                a = promotion.Promotion(piece)
                                a.mainloop()
                                board[current_move[1][1]][current_move[1][0]] = a.getPromote()
                        board[current_move[0][1]][current_move[0][0]] = "--"
                        white_turn = not white_turn
                    

                    if piece_name == "wK":
                        engine.whiteKingPos = (new_row,new_col)
                        engine.white_king_moved = True
                        engine.white_king_counter +=1

                    if piece_name == "bK":
                        engine.blackKingPos = (new_row,new_col)
                        engine.black_king_moved = True
                        engine.black_king_counter +=1

                    if piece_name == "bR" and (start_row,start_col) == engine.black_rook1_pos:

                        engine.black_rook1_moved = True
                        engine.black_rook1_counter +=1 
                        engine.black_rook1_pos = (new_row,new_col)
                    if piece_name == "bR" and (start_row,start_col) == engine.black_rook2_pos:
                        engine.black_rook2_moved = True
                        engine.black_rook2_counter +=1
                        engine.black_rook2_pos = (new_row,new_col)

                    if piece_name == "wR" and(start_row,start_col) == engine.white_rook1_pos:
                        engine.white_rook1_moved = True
                        engine.white_rook1_counter +=1
                        engine.white_rook1_pos = (new_row,new_col)

                    if piece_name == "wR" and (start_row,start_col) == engine.white_rook2_pos:
                        engine.white_rook2_moved = True
                        engine.white_rook2_counter +=1
                        engine.white_rook2_pos = (new_row,new_col)

                    if piece == "w":
                        all_possible_moves_enemy = chess.moves().all_possible_valid_moves(board,enemy,engine.blackKingPos)
                        inCheck = chess.moves().inCheck(board,engine.blackKingPos)
                        if inCheck:
                            check_sq = engine.blackKingPos
                        else:
                            check_sq = ()
                        if len(all_possible_moves_enemy) == 0 and not inCheck:
                            engine.stalemate = True
                        elif len(all_possible_moves_enemy) == 0 and inCheck:
                            engine.white_checkmate = True

                    else:
                        all_possible_moves_enemy = chess.moves().all_possible_valid_moves(board,enemy,engine.whiteKingPos)
                        inCheck = chess.moves().inCheck(board,engine.whiteKingPos)
                        if inCheck:
                            check_sq = engine.whiteKingPos
                        else:
                            check_sq = ()
                        if len(all_possible_moves_enemy) == 0 and not inCheck:
                            engine.stalemate = True
                        elif len(all_possible_moves_enemy) == 0 and inCheck:
                            engine.black_checkmate = True


                    valid_move = []
                    counts.append(count)


                highlight_sq = []
                current_move = []
                valid_move = []
                special_move = []
                special_pawn = []

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if len(engine.moves)!=0:
                    count = 0
                    if len(counts)!=0:
                        count = counts.pop()
                    move = engine.moves.pop()
                    valid_move = []

                    if  move.white_enPassant:
                        board[move.start_row][move.start_col] = "wP"
                        board[move.end_row][move.end_col] = "--"
                        board[move.end_row+1][move.end_col] = "bP"
                        engine.white_enPassant = True
                        white_turn = not white_turn
                        if len(engine.moves)!=0:
                            EP = engine.moves[-1]
                            if EP.piece_moved == "wP":
                                if len(white_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(white_enPassant,count)
                                    if count ==2 and len(white_enPassant)>1:
                                        pop_n_times(white_enPassant,count)

                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.black_enPassant = True
                            if EP.piece_moved == "bP":
                                if len(black_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(black_enPassant,count)
                                    if count ==2 and len(black_enPassant)>1:
                                        pop_n_times(black_enPassant,count)
                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.white_enPassant = True


                    elif move.black_enPassant:
                        board[move.start_row][move.start_col] = move.piece_moved
                        board[move.end_row][move.end_col] = move.piece_captured
                        board[move.end_row-1][move.end_col] = "wP"
                        engine.black_enPassant = True
                        white_turn = not white_turn

                        if len(engine.moves)!=0:
                            EP = engine.moves[-1]
                            if EP.piece_moved == "wP":
                                if len(white_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(white_enPassant,count)
                                    if count ==2 and len(white_enPassant)>1:
                                        pop_n_times(white_enPassant,count)

                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.black_enPassant = True
                            if EP.piece_moved == "bP":

                                if len(black_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(black_enPassant,count)
                                    if count ==2 and len(black_enPassant)>1:
                                        pop_n_times(black_enPassant,count)
                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.white_enPassant = True

                    elif not move.castle_move:

                        engine.white_enPassant = False
                        engine.black_enPassant = False
  


                        board[move.start_row][move.start_col] = move.piece_moved
                        board[move.end_row][move.end_col] = move.piece_captured
                        white_turn = not white_turn
                        #en passant check
                        if len(engine.moves)!=0:
                            EP = engine.moves[-1]
                            if EP.piece_moved == "wP":
                    
                                if len(white_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(white_enPassant,count)
                                    if count ==2 and len(white_enPassant)>1:
                                        pop_n_times(white_enPassant,count)
                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.black_enPassant = True
                            if EP.piece_moved == "bP":
                                if len(black_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(black_enPassant,count)
                                    if count ==2 and len(white_enPassant)>1:
                                        pop_n_times(black_enPassant,count)
                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.white_enPassant = True
                        if move.piece_moved == "wK":
                            engine.whiteKingPos = (move.start_row,move.start_col)
                            engine.white_king_counter -=1
                            if engine.white_king_counter == 0:
                                engine.white_king_moved = False
                        elif move.piece_moved == "bK":
                            engine.blackKingPos = (move.start_row,move.start_col)
                            engine.black_king_counter -=1
                            if engine.black_king_counter == 0:
                                engine.black_king_moved = False

                        elif move.piece_moved == "wR" and engine.white_rook1_pos == (move.end_row,move.end_col):
                            engine.white_rook1_pos = (move.start_row,move.start_col)
                            engine.white_rook1_counter -=1
                            if engine.white_rook1_counter == 0 :
                                engine.white_rook1_moved = False
                        elif move.piece_moved == "wR" and engine.white_rook2_pos == (move.end_row,move.end_col):
                            engine.white_rook2_pos = (move.start_row,move.start_col)
                            engine.white_rook2_counter -=1
                            if engine.white_rook2_counter == 0:
                                engine.white_rook2_moved = False

                        elif move.piece_moved == "bR" and engine.black_rook1_pos == (move.end_row,move.end_col):
                            engine.black_rook1_pos = (move.start_row,move.start_col)
                            engine.black_rook1_counter -=1
                            if engine.black_rook1_counter == 0 :
                                engine.black_rook1_moved = False

                        elif move.piece_moved == "bR" and engine.black_rook2_pos == (move.end_row,move.end_col):
                            engine.black_rook2_pos = (move.start_row,move.start_col)
                            engine.black_rook2_counter -=1
                            if engine.black_rook2_counter == 0 :
                                engine.black_rook2_moved = False


                    else:   #castle undo
                        engine.white_enPassant = False
                        engine.black_enPassant = False
                        board[move.start_row][move.start_col] = move.piece_moved
                        board[move.end_row][move.end_col] = move.piece_captured
                        white_turn = not white_turn
                        if len(engine.moves)!=0:
                            EP = engine.moves[-1]
                            if EP.piece_moved == "wP":
                                if len(white_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(white_enPassant,count)
                                    if count ==2 and len(white_enPassant)>1:
                                        pop_n_times(white_enPassant,count)
                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.black_enPassant = True
                            if EP.piece_moved == "bP":
                                if len(black_enPassant)!=0:
                                    if count == 1:
                                        pop_n_times(black_enPassant,count)
                                    if count ==2 and len(black_enPassant)>1:
                                        pop_n_times(black_enPassant,count)

                                if chess.moves().enPassant_move(board,(EP.start_row,EP.start_col), (EP.end_row,EP.end_col),EP.piece_moved):
                                    engine.white_enPassant = True
                        if move.piece_moved == "wK":
                            engine.whiteKingPos = (move.start_row,move.start_col)
                            engine.white_king_moved = False
                            engine.white_king_counter -=1

                        elif move.piece_moved == "bK":
                            engine.blackKingPos = (move.start_row,move.start_col)
                            engine.black_king_moved = False
                            engine.black_king_counter -=1

                        if move.end_col == 2:
                            board[move.end_row][0] = board[move.end_row][move.end_col+1]
                            board[move.end_row][move.end_col+1] = "--"
                        elif move.end_col == 6:
                            board[move.end_row][7] = board[move.end_row][move.end_col-1]
                            board[move.end_row][move.end_col-1] = "--"            
                    inCheck = chess.moves().inCheck(board,engine.blackKingPos)
                    if inCheck:
                        check_sq = engine.blackKingPos
                    else:
                        check_sq = ()
                    if not inCheck:
                        inCheck = chess.moves().inCheck(board,engine.whiteKingPos)
                        if inCheck:
                            check_sq = engine.whiteKingPos
                        else:
                            check_sq = ()



    drawboard()
    drawPieces()
    pygame.display.update()

    if engine.black_checkmate:
        messagebox.showinfo("GameOver", "Checkmate, Black Wins.") 
        engine.black_checkmate = False
    if engine.white_checkmate:
        messagebox.showinfo("GameOver", "Checkmate, White Wins.") 
        engine.white_checkmate = False
    if engine.stalemate:
        messagebox.showinfo("GameOver", "Draw By STALEMATE.") 
        engine.stalemate = False


