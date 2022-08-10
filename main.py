#importing pygame
import pygame

#initialising the window and configuring its details
def create_screen():
    pygame.init()
    canvas = pygame.display.set_mode((650, 650))
    pygame.display.set_caption("Chess Game")
    img = pygame.image.load("blackking.png")
    pygame.display.set_icon(img) 
    pygame.mouse.set_cursor(pygame.cursors.arrow)

    return canvas

def load_background():
    image = pygame.image.load("chessboard.jpg")
    image = pygame.transform.scale(image, (650,650))
    return image

#function which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
#returns the event
def mouse_up_down(type):
    received = False
    while not received:
        for event in pygame.event.get():
            if type == "down":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return event
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.time.delay(10)
                    return event 

#class that contains the square blocks on the chessboard
class square:
    def __init__(self, x, y):
        #determines the position of the square on the chessboard and creates a rect to represent the square
        self.rect = pygame.Rect((x*65+63, y*65+63), standard)
        #determines the status of the square
        self.status = "empty"
        self.sqr_in_check_black = False
        self.sqr_in_check_white = False

#class containing the promotion choices
class choice:
    def __init__(self, color, position, type_piece):
        #loading the object's image
        self.img = load_chess_piece(color + type_piece + ".png")
        #creating a rect around the image and changing the position to match the image's position
        self.rect = self.img.get_rect(topleft = position)
        self.type = type_piece
        #placing the image onto the board
        canvas.blit(self.img, dest = self.rect)
        
#class that contains classes for each of the types of chess pieces
class chess:
    def __init__(self, color, square, type):
        self.color = color
        chess_pieces.append(self)
        position = square.rect
        self.moved = False
        #loading the object's image
        file_name = self.color + type + ".png"
        self.img = load_chess_piece(file_name)
        #placing the image onto the board
        canvas.blit(self.img, dest = position) 
        #creating a rect around the image and changing the position to match the image's position
        self.rect = self.img.get_rect(topleft = (position[0], position[1]))
        #creating a centre point so that the appropriate square the chess piece is moved to can be allocated accurately
        #this means that the chess piece can be made to sit exactly inside a square, even if not placed exactly inside the square by the user. 
        self.rect_centre = pygame.Rect(self.rect[0]+35, self.rect[1]+35, 1, 1)

    #function that finds the available moves of a piece from a list of possible moves
    def find_moves(self, moves, special_moves):
        available_moves = []
        i = 0
        length = len(moves)
        while i < length:
            #checking whether the square coordinates are within the existing range of square coordinates
            if moves[i][0] >= 0 and moves[i][0] <= 7 and moves[i][1] >= 0 and moves[i][1] <= 7:
                chessboard_sqr = chessboard[moves[i][0]][moves[i][1]]
                #checking whether the square contains a chess piece and checking its colour
                #this is so that only empty squares and squares containing a different color than the chess piece (that is not the king) are added to the avaliable moves list
                if chessboard_sqr.status != "empty":
                    #print(chessboard_sqr.status)
                    if chessboard_sqr.status.color != self.color and not isinstance(chessboard_sqr.status, chess.king):
                        available_moves.append(moves[i])
                    #if the chess piece on the chessboard is a king of the opposite color, the king will be in check
                    #the 'King in Check' statement along with the coordinates of the chessboard square the king is on are added to the 'special_moves' list
                    elif chessboard_sqr.status.color != self.color and isinstance(chessboard_sqr.status, chess.king):
                        special_moves.append(["King in Check", moves[i]])
                    #checks whether the chess piece on the chessboard is not a king and of the same color as the chess piece being moved
                    #if so, the square will not be available for the piece to move to, but is still counted as 'in check' for the king of the opposite color
                    elif chessboard_sqr.status.color == self.color and not isinstance(chessboard_sqr.status, chess.king):
                        special_moves.append(["Square in Check", moves[i]])
                else:
                    available_moves.append(moves[i])
            i += 1
        return available_moves, special_moves

    #function that finds the diagonal 'bishop-like' movements of a piece (for the bishop and queen)
    def bishop_moves(self, moves, x, y, special_moves):
        pos_x_diag_raw = []
        pos_minus_x_diag_raw = []
        neg_x_diag_raw = []
        neg_minus_x_diag_raw = []
        #finds the coordinates for the movement up till 7 squares in four different diagonal directions
        for i in range (-7, 0):
            pos_x_diag_raw.append([x-i, y+i])
            pos_minus_x_diag_raw.append([x+i, y+i])
        for j in range (0, 8):
            neg_x_diag_raw.append([x-j, y+j])
            neg_minus_x_diag_raw.append([x+j, y+j])

        #function that checks whether each coordinate in a diagonal list of coordinates corresponds to a real chessboard square coordinate
        def check(diag):
            diags = []
            for i in range (0, len(diag)):
                if diag[i][0] >= 0 and diag[i][0] <= 7 and diag[i][1] >= 0 and diag[i][1] <= 7:
                    diags.append(diag[i])
            return diags

        #filtering out the invalid coordinates in each diagonal
        pos_x_diag = check(pos_x_diag_raw)
        pos_minus_x_diag = check(pos_minus_x_diag_raw)
        neg_x_diag = check(neg_x_diag_raw)
        neg_minus_x_diag = check(neg_minus_x_diag_raw)

        #function that moves through the diagonal from beginning to end
        #it keeps adding the square coordinates to the list 'moves' until (and including) a chessboard square with a piece on it is reached or until the end of the diagonal list has been reached
        #it then returns 'moves'
        def find_bishop_movements_r(moves, diag, coor):
            empty_found = False
            i = len(diag)-1
            while i >= 0 and not empty_found:
                moves.append(diag[i])
                if chessboard[diag[i][0]][diag[i][1]].status != "empty" and diag[i] != coor:
                    empty_found = True
                i -= 1
            return moves

        #function that moves through the diagonal from end to beginning
        #it keeps adding the square coordinates to the list 'moves' until (and including) a chessboard square with a piece on it is reached or until the beginning of the diagonal list has been reached
        #it then returns 'moves'
        def find_bishop_movements_l(moves, diag, coor):
            empty_found = False
            i = 0
            while i < len(diag) and not empty_found:
                moves.append(diag[i])
                if chessboard[diag[i][0]][diag[i][1]].status != "empty" and diag[i] != coor:
                    empty_found = True
                i += 1
            return moves

        #finds the movements the chess piece can make on each diagonal, appending them to the list 'moves'
        moves = find_bishop_movements_r(moves, pos_minus_x_diag, [x,y])
        moves = find_bishop_movements_l(moves, neg_minus_x_diag, [x,y])
        moves = find_bishop_movements_r(moves, pos_x_diag, [x,y])
        moves = find_bishop_movements_l(moves, neg_x_diag, [x,y])

        #calls find_moves() to check whether the moves can be made
        return chess.find_moves(self, moves, special_moves)

    #function that finds the horizontal and vertical 'rook-like' movements of a piece (for the rook and queen)
    def rook_moves(self, moves, x, y, special_moves):
        row = []
        col = []
        #creates a list of the square coordinates in the same row as the rook
        #creates a list of the square coordinates in the same column as the rook
        for i in range (0, 8):
            row.append([i, y])
            col.append([x, i])

        #function that moves through the row/column from end to beginning and from beginning to end
        #finds the moves the rook can make on the row/column
        def find_rook_movements(moves, row_col, coor):
            moves1 = []
            #runs through the row/column from beginning to end
            #creates it keeps adding the square coordinates to the list 'moves1' until (and including) a chessboard square with a piece on it is reached or until the end of the row/column list has been reached
            empty_found = False
            i = 7
            while i > -1 and not empty_found:
                moves1.append(row_col[i])
                if chessboard[row_col[i][0]][row_col[i][1]].status != "empty" and i < coor:
                    empty_found = True
                i -= 1

            moves2 = []
            #runs through the row/column from end to beginning
            #creates it keeps adding the square coordinates to the list 'moves2' until (and including) a chessboard square with a piece on it is reached or until the beginning of the row/column list has been reached
            empty_found = False
            i = 0
            while i < 8 and not empty_found:
                moves2.append(row_col[i])
                if chessboard[row_col[i][0]][row_col[i][1]].status != "empty" and i > coor:
                    empty_found = True
                i += 1

            #searches through the lists 'moves1' and 'moves2' and adds the coordinates that are in both lists to the list 'moves'
            #this is so that only the square coordinates that are in between two chess pieces (or the two ends of the chessboard row/column or an end of the chessboard row/column and a chess piece) are added to the list
            for i in range (0, len(moves1)):
                for j in range (0, len(moves2)):
                    if moves1[i] == moves2[j]:
                        moves.append(moves1[i])

            return moves

        #finds the movements the rook can make on the row and column, appending them to the list 'moves'
        moves = find_rook_movements(moves, row, x)
        moves = find_rook_movements(moves, col, y)

        #calls find_moves() to check whether the moves can be made
        return chess.find_moves(self, moves, special_moves)

    #procedure that performs castling
    #works for both when the rook and the king are the first to be selected.
    def castling(self, special_moves, clicked, other_piece):
            #decides which side of the chessboard the castling will be done and decides two new chessboard squares for the chess pieces
            if special_moves[2] == "r":
                new_pos = chessboard[6][clicked[1]]
                new_pos2 = chessboard[5][clicked[1]]
            else:
                new_pos = chessboard[2][clicked[1]]
                new_pos2 = chessboard[3][clicked[1]]
            
            #checks which piece is a rook and which is a king
            if isinstance(other_piece, chess.rook):
                rook = other_piece
                king = self
                #erases the spot the king/rook was initially moved to (in this case the rook)
                canvas.blit(background, king.rect, king.rect)
            else:
                rook = self
                king = other_piece
                #erases the spot the king/rook was initially moved to (in this case the king)
                canvas.blit(background, rook.rect, rook.rect)
            other_piece.moved = True

            #loads the king's image onto its new position on the board
            #moves the king's rect and centre rect to this chessboard square as well
            canvas.blit(king.img, new_pos.rect)
            king.rect = king.rect.move(-king.rect[0]+new_pos.rect[0], -king.rect[1]+new_pos.rect[1])
            king.rect_centre = king.rect_centre.move(-king.rect_centre[0]+king.rect[0]+35, -king.rect_centre[1]+king.rect[1]+35)
            #updates the new position chessboard square status to contain the king
            new_pos.status = king

            #loads the rook's image onto its new position on the board
            #moves the rook's rect and centre rect to this chessboard square as well
            canvas.blit(rook.img, new_pos2.rect)
            rook.rect = rook.rect.move(-rook.rect[0]+new_pos2.rect[0], -rook.rect[1]+new_pos2.rect[1])
            rook.rect_centre = rook.rect_centre.move(-rook.rect_centre[0]+rook.rect[0]+35, -rook.rect_centre[1]+rook.rect[1]+35)
            #updates the new position chessboard square status to contain the rook
            new_pos2.status = rook
            
            #sets the chessboard square status where the king/rook was before to 'empty'
            chess_square.status = "empty"  
    
    #procedure that updates the 'in check' status of each chessboard square for both kings
    def update_check():
        #procedure that finds the areas 'in check' (for both kings) by each piece on the chessboard square
        #updates the chessboard square sqr_in_check_black or sqr_in_check_white to True if it is in check for the king of that particular color
        def find_in_check(a, b, available_moves, special_moves):
            #checks whether the chess piece is a pawn
            if isinstance(chessboard[a][b].status, chess.pawn):
                #finds the 'in check pawn' special moves which contain the diagonal moves of the pawn 
                for diag in special_moves:
                    if diag[0] == "in check pawn":
                        #checks the color of the pawn 
                        if chessboard[a][b].status.color == "white":
                            #updates the chessboard square sqr_in_check_black to True because the black king would be in check on the diagonal from the white pawn
                            chessboard[diag[1][0]][diag[1][1]].sqr_in_check_black = True
                        else:
                            #updates the chessboard square sqr_in_check_white to True because the white king would be in check on the diagonal from the black pawn
                            chessboard[diag[1][0]][diag[1][1]].sqr_in_check_white = True
            #if the chesspiece is not a pawn:
            else:
                #removes the castling move if there is one (click on the king from a selected rook or click on the rook from a selected king)
                to_remove = []
                #checks whether the chess piece is a king and has not been moved before or if it is a rook and has not been moved before
                if isinstance(chessboard[a][b].status, chess.king) and chessboard[a][b].status.moved == False or isinstance(chessboard[a][b].status, chess.rook) and chessboard[a][b].status.moved == False:
                    #removes any castling moves there are
                    for i in range(0, len(available_moves)):
                        if available_moves[i] == [7, b]:
                            to_remove.append([7, b])
                        elif available_moves[i] == [0, b]:
                            to_remove.append([0, b])

                    for i in range (0, len(to_remove)):
                        available_moves.remove(to_remove[i])

                #checks whether the 'special_moves' list contains any 'King in Check' statements
                #this means that the chess piece is in a position where the king of the opposing color is in check
                for i in range (0, len(special_moves)):
                    if special_moves[i][0] == "King in Check":
                        available_moves.append(special_moves[i][1])

                #checks whether the 'special_moves' list contains any 'Square in Check' statements
                #this means that the chess piece is in a position where there is another piece of the same color standing on a square that is in check
                #this is needed so that a king cannot step on a square that is occupied by a piece of the opposite color, but in check
                for i in range (0, len(special_moves)):
                    if special_moves[i][0] == "Square in Check":
                        available_moves.append(special_moves[i][1])

                #updates the chessboard square 'in check' values for each move in the available moves of the chess piece
                for k in range(0, len(available_moves)):
                    #checks the color of the chess piece
                    if chessboard[a][b].status.color == "white":
                        #updates the chessboard square sqr_in_check_black to True because the black king would be in check on a square to which a white chess piece (except a pawn) can move to
                        chessboard[available_moves[k][0]][available_moves[k][1]].sqr_in_check_black = True
                    else:
                        #updates the chessboard square sqr_in_check_white to True because the white king would be in check on a square to which a black chess piece (except a pawn) can move to                                            
                        chessboard[available_moves[k][0]][available_moves[k][1]].sqr_in_check_white = True

        #resets all of the chessboard squares' sqr_in_check_black or sqr_in_check_white to False
        for a in range (0, len(chessboard)):
            for b in range(0, len(chessboard)): 
                chessboard[a][b].sqr_in_check_white = False
                chessboard[a][b].sqr_in_check_black = False

        #loops through the chessboard squares and updates the chessboard square areas 'in check' (for both kings)
        #this is done by changing the value of the chessboard square's sqr_in_check_black or sqr_in_check_white
        for a in range (0, len(chessboard)):
            for b in range(0, len(chessboard)): 
                #checks whether the chessboard square is not empty
                if chessboard[a][b].status != "empty":
                    #finds the available moves and special moves (if there are any) of the chess piece from its current position
                    special_moves = []
                    available_moves_and_special_moves = chessboard[a][b].status.moves(a, b, special_moves)
                    available_moves = available_moves_and_special_moves[0]
                    special_moves = available_moves_and_special_moves[1]
                    
                    #calls find_in_check() to find the areas in check by the chess piece and update their sqr_in_check_black or sqr_in_check_white values
                    find_in_check(a, b, available_moves, special_moves)
    
    #function which checks the 'available_moves' list passed in and returns only the movements that would not result in the king (of the same color as the piece) being in check 
    def check_check(self, current, available_moves):
        #function that checks whether the chessboard square with the king (passed in) is in check for the king's color
        #returns True is it is
        def king_sqr_in_check(self, king_square):
            if self.color == "white":
                king_square_in_check = king_square.sqr_in_check_white
            else:
                king_square_in_check = king_square.sqr_in_check_black

            if king_square_in_check:
                return True

        #sets the status of the chessboard square containing the piece to "empty"
        current.status = "empty"
        possible_moves = []
        #checks each move in the 'available_moves' list
        for i in range (0, len(available_moves)):
            #assigns the value of the status of the square of a move in the list 'available_moves' to the variable 'old_piece'
            old_piece = chessboard[available_moves[i][0]][available_moves[i][1]].status

            #assigns the piece to the status of the square
            chessboard[available_moves[i][0]][available_moves[i][1]].status = self
                        
            #calls update_check() to update the 'in check' values of each chessboard square
            chess.update_check()

            if self.color == "white":
                kingpos = find_piece(whiteking)
            elif self.color == "black":
                kingpos = find_piece(blackking)

            #the chessboard square contained the king is assigned to the variable 'king_square'
            king_square = chessboard[kingpos[0]][kingpos[1]]
                
            #calls king_square_in_check() to check whether the king of the same color as the piece is in check
            king_square_in_check = king_sqr_in_check(self, king_square)

            #if the king is not in check, the move is appended to the list of possible_moves
            #this is because the piece should never move to expose the king to an enemy pieces' attack and should be able to block an attack
            if not king_square_in_check:
                possible_moves.append(available_moves[i])

            #the status of the chessboard square that was tested is set to the old_piece again, returing its state to the state it had before it was tested
            chessboard[available_moves[i][0]][available_moves[i][1]].status = old_piece
            
        #the status of the chessboard square that originally contained the chess piece is set to the chess piece again, returning its state to the state it has before it was tested
        current.status = self

        return possible_moves
        
    #procedure that checks whether the king passed in is in checkmate or stalemate
    def check_checkmate_stalemate(king):

        """add comments/modify"""
        #finds the king's position and the king's possible moves and the moves the king would be able to take if the 'in check' status (for the color of the king) of the all chessboard squares was ignored
        king_pos = find_piece(king)
        king_moves_without_in_check = king.moves(king_pos[0], king_pos[1], [])[0]
        king_moves = chess.check_check(king, chessboard[king_pos[0]][king_pos[1]], king_moves_without_in_check)

        # function that finds and returns the 'in check' status of the chessboard square containing the king for the color of the king
        def find_king_sqr(king, king_pos):
            if king.color == "white":
                king_sqr = chessboard[king_pos[0]][king_pos[1]].sqr_in_check_white
            else:
                king_sqr = chessboard[king_pos[0]][king_pos[1]].sqr_in_check_black
            return king_sqr

        #checks whether the king has no moves but would have had moves if the 'in check' status of the all chessboard squares was ignored
        #this means that the king is completely surrounded by chessboard squares that are 'in check'
        if king_moves == []:
        #if king_moves == [] and king_moves_without_in_check != []:
            #calls find_king_sqr to find the 'in check' status (for the color of the king) of the chessboard square the king is on
            king_sqr = find_king_sqr(king, king_pos)
            
            found = False
            a = 0
            b = 0
            #searching through the chess pieces of the same color as the king
            #the chess pieces are searched until there are no more chess pieces to check or until a chess piece that, if moved to a position, would allow the king to move to another chessboard square is found
            while not found and a < 8:
                if chessboard[a][b].status != "empty":
                    #checks whether the chess piece color matches that of the king
                    if chessboard[a][b].status.color == king.color and not isinstance(chessboard[a][b].status, chess.king):
                        #finds the moves that the chess piece could take
                        piece = chessboard[a][b].status
                        available_moves = piece.moves(a, b, [])[0] 
                    
                        #sets the status of the chessboard square containing the piece to "empty"
                        chessboard[a][b].status = "empty" 

                        #checks each move in the 'available_moves' list
                        for i in range (0, len(available_moves)):
                            #assigns the value of the status of the square of a move in the list 'available_moves' to the variable 'old_piece'
                            old_piece = chessboard[available_moves[i][0]][available_moves[i][1]].status
                            #assigns the piece to the status of the square
                            chessboard[available_moves[i][0]][available_moves[i][1]].status = piece

                            #calls update_check() to update the 'in check' values of each chessboard square
                            chess.update_check()

                            #finds the moves the king would have with this new positioning
                            new_king_moves_without_in_check = king.moves(king_pos[0], king_pos[1], [])[0]
                            #print(new_king_moves_without_in_check)
                            new_king_moves = chess.check_check(king, chessboard[king_pos[0]][king_pos[1]], new_king_moves_without_in_check)
                            #if the king can move to other chessboard square and the king was not originally in check, found is set to True and the loop is ended

                            if new_king_moves != [] and not king_sqr:
                                #print(new_king_moves, chessboard[new_king_moves[0][0]][new_king_moves[0][1]].sqr_in_check_white)
                                #print(chess.check_check(king, chessboard[king_pos[0]][king_pos[1]], new_king_moves))
                                found = True

                            #if the king can move to other chessboard square and the king was originally in check, then the 'in check' status  of the chessboard square (for the current positioning) the king is on is found 
                            elif new_king_moves != [] and king_sqr:
                                # if the king is not in check in the current position, found is set to True and the loop is ended
                                if not find_king_sqr(king, king_pos):
                                    found = True

                            #the status of the chessboard square that was tested is set to the old_piece again, returing its state to the state it had before it was tested
                            chessboard[available_moves[i][0]][available_moves[i][1]].status = old_piece

                        #the status of the chessboard square that originally contained the chess piece is set to the chess piece again, returning its state to the state it has before it was tested
                        chessboard[a][b].status = piece
                            
                b += 1
                if b == 8:
                    b = 0
                    a += 1

            #if a chess piece that, if moved to a position, would allow the king to move to another chessboard square (that would stop the king from being in check), is not found and the king is in check, the king is in checkmate
            if not found and king_sqr:
                print("checkmate")
            #if a chess piece that, if moved to a position, would allow the king to move to another chessboard square is not found and the king is not check, the king is in stalemate
            if not found and not king_sqr:
                print("stalemate")

    #class for the kings
    class king:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "king")

        #function adds the castling move
        def add_castling(self, x, y, moves, special_moves):
            #finds the 'in check' status of the chessboard square the king is on for the king's color
            if self.color == "white":
                in_check = chessboard[x][y].sqr_in_check_white
            else:
                in_check = chessboard[x][y].sqr_in_check_black

            #checks whether the king has been moved before and is not in check
            if self.moved == False and not in_check:
                #finds the 'in check' status (for the color of the king) for the chessboard square blocks the king would be passing through/landing on when castling
                if self.color == "white":
                    moving_r_1_check = chessboard[5][y].sqr_in_check_white
                    moving_r_2_check = chessboard[6][y].sqr_in_check_white
                    moving_l_1_check = chessboard[3][y].sqr_in_check_white
                    moving_l_2_check = chessboard[2][y].sqr_in_check_white
                else:
                    moving_r_1_check = chessboard[5][y].sqr_in_check_black
                    moving_r_2_check = chessboard[6][y].sqr_in_check_black
                    moving_l_1_check = chessboard[3][y].sqr_in_check_black
                    moving_l_2_check = chessboard[2][y].sqr_in_check_black

                #checks whether there is no chess piece between the king and the piece at the right end of the chessboard (also checks whether there is a piece at the last position of the row)
                #also checks that the king will not pass through/finish at any chessboard squares under attack by an enemy piece while castling
                if chessboard[5][y].status == "empty" and chessboard[6][y].status == "empty" and chessboard[7][y].status != "empty" and not moving_r_1_check and not moving_r_2_check:
                    #checks whether the last piece is a rook and whether it has not been moved before
                    if isinstance(chessboard[7][y].status, chess.rook):
                        if not chessboard[7][y].status.moved:
                            #appends the chessboard square coordinates of the last piece and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                            special_moves.append(["castling", [7, y], "r"])
                            #appends the chessboard square coordinates of the last piece to the list 'moves'
                            moves.append([7, y])
                #checks whether there is no chess piece between the king and the piece at the left end of the chessboard (also checks whether there is a piece at the first position of the row)
                #also checks that the king will not pass through/finish at any chessboard squares under attack by an enemy piece while castling
                if chessboard[3][y].status == "empty" and chessboard[2][y].status == "empty" and chessboard[1][y].status == "empty" and chessboard[0][y].status != "empty" and not moving_l_1_check and not moving_l_2_check:
                    #checks whether the first piece is a rook and whether it has not been moved before
                    if isinstance(chessboard[0][y].status, chess.rook):
                        if not chessboard[0][y].status.moved:
                            #appends the chessboard square coordinates of the first piece and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                            special_moves.append(["castling", [0, y], "l"])
                            #appends the chessboard square coordinates of the first piece to the list 'moves'
                            moves.append([0, y])

            return moves, special_moves

            
        #takes in the current square coordinates the king is in
        #returns the coordinates of the chessboard squares the king can move to
        def moves(self, x, y, special_moves):
            moves_1 = []
            for i in range (-1, 2):
                for j in range (-1, 2):
                    moves_1.append([x+j, y+i])
            moves_1.remove([x, y])

            #calls find_moves() to check whether the moves can be made
            moves_and_special_moves = chess.find_moves(self, moves_1, special_moves)
            moves = moves_and_special_moves[0]

            #sets 'special_moves' to the special moves (the check) returned from the find_moves() function
            special_moves = moves_and_special_moves[1]

            #returns the moves the king can take, the special moves, and the moves the king would be able to take if the 'in check' status (for the color of the king) of the all chessboard squares was ignored
            return moves, special_moves

    #class for the queens
    class queen:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "queen")

        #takes in the current square coordinates the queen is in
        #returns the coordinates of the chessboard squares the queen can move to
        def moves(self, x, y, special_moves):
            moves = []
            #calls bishop_moves() to find the queen's diagonal movements
            moves_and_special_moves =  chess.bishop_moves(self, moves, x, y, special_moves)
            moves = moves_and_special_moves[0]
            #sets 'special_moves' to the special moves (the check) returned from the find_moves() function
            special_moves = moves_and_special_moves[1]

            # #calls rook_moves() to find the queen's horizontal and vertical movements
            moves_and_special_moves = chess.rook_moves(self, moves, x, y, special_moves)
            moves = moves_and_special_moves[0]

            #appends the special moves (the check) returned from the find_moves() function to the list 'special_moves' 
            for i in range (0, len(moves_and_special_moves[1])):
                special_moves.append(moves_and_special_moves[1][i])
            
            #returns the queen's movements and special_moves
            return moves, special_moves
           
    #class for the bishops   
    class bishop:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "bishop")

        #takes in the current square coordinates the bishop is in
        #returns the coordinates of the chessboard squares the bishop can move to
        def moves(self, x, y, special_moves):
            moves = []
            #calls bishop_moves() to find the bishop's moves
            moves_and_special_moves = chess.bishop_moves(self, moves, x, y, special_moves) 
            moves = moves_and_special_moves[0]
            #sets 'special_moves' to the special moves (the check) returned from the find_moves() function
            special_moves = moves_and_special_moves[1] 
            return moves, special_moves

    #class for the knights
    class knight:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "knight")

        #takes in the current square coordinates the knight is in
        #returns the coordinates of the chessboard squares the knight can move to
        def moves(self, x, y, special_moves):
            moves = []
            for i in range (-2, 0):
                moves.append([x+i, y+3+i]) 
                moves.append([x-i, y-3-i])
            moves.append([x+1, y+2])
            moves.append([x+2, y+1])
            moves.append([x-2, y-1])
            moves.append([x-1, y-2])

            #calls find_moves() to check whether the moves can be made
            moves_and_special_moves = chess.find_moves(self, moves, special_moves)
            moves = moves_and_special_moves[0]
            #sets 'special_moves' to the special moves (the check) returned from the find_moves() function
            special_moves = moves_and_special_moves[1]

            return moves, special_moves

    #class for the rooks
    class rook:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "rook")

        #function adds the castling move
        def add_castling(self, x, y, moves, special_moves):
            #checks whether the rook has been moved before
            if self.moved == False:
                #checks whether there is a piece at 4th position of the row
                if chessboard[4][y].status != "empty":
                    #checks whether the piece on the 4th position of the chessboard row is a king and whether it has not been moved before
                    if isinstance(chessboard[4][y].status, chess.king) and not chessboard[4][y].status.moved:
                        #finds the 'in check' status of the chessboard square the king is on for the king's color
                        if chessboard[4][y].status.color == "white":
                            in_check = chessboard[4][y].sqr_in_check_white
                        else:
                            in_check = chessboard[4][y].sqr_in_check_black

                        if not in_check:
                            #finds the 'in check' status (for the color of the king) for the chessboard square blocks the king would be passing through/landing on when castling
                            if self.color == "white":
                                moving_r_1_check = chessboard[5][y].sqr_in_check_white
                                moving_r_2_check = chessboard[6][y].sqr_in_check_white
                                moving_l_1_check = chessboard[3][y].sqr_in_check_white
                                moving_l_2_check = chessboard[2][y].sqr_in_check_white
                            else:
                                moving_r_1_check = chessboard[5][y].sqr_in_check_black
                                moving_r_2_check = chessboard[6][y].sqr_in_check_black
                                moving_l_1_check = chessboard[3][y].sqr_in_check_black
                                moving_l_2_check = chessboard[2][y].sqr_in_check_black

                            #checks whether the rook is the last one in the row, or the first one in the row
                            if x == 7:
                                #checks whether there is no chess piece between the rook and the king
                                #also checks that the king will not pass through/finish at any chessboard squares under attack by an enemy piece while castling
                                if chessboard[6][y].status == "empty" and chessboard[5][y].status == "empty" and not moving_r_1_check and not moving_r_2_check:
                                    #appends the chessboard square coordinates of the king and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                                    special_moves.append(["castling", [4, y], "r"])
                                    #appends the chessboard square coordinates of the king to the list 'moves'
                                    moves.append([4, y])
                            elif x == 0:
                                #checks whether there is no chess piece between the rook and the king
                                #also checks that the king will not pass through/finish at any chessboard squares under attack by an enemy piece while castling
                                if chessboard[1][y].status == "empty" and chessboard[2][y].status == "empty" and chessboard[3][y].status and not moving_l_1_check and not moving_l_2_check:
                                    #appends the chessboard square coordinates of the king and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                                    special_moves.append(["castling", [4, y], "l"])
                                    #appends the chessboard square coordinates of the king to the list 'moves'
                                    moves.append([4, y])

            return moves, special_moves
        
        #takes in the current square coordinates the rook is in
        #returns the coordinates of the chessboard squares the rook can move to
        def moves(self, x, y, special_moves): 
            moves = []
            #calls rook_moves() to find the rook's moves
            moves_and_special_moves = chess.rook_moves(self, moves, x, y, special_moves)
            #calls find_moves() to check whether the moves can be made
            moves = moves_and_special_moves[0]
            #sets 'special_moves' to the special moves (the check) returned from the find_moves() function
            special_moves = moves_and_special_moves[1]
                    
            return moves, special_moves
        
    #class for the pawns
    class pawn:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "pawn")
            self.enpassant = "no capture"

        #promotes the pawn to another chess piece
        def promote(self, chess_square):
            #checks the color of the pawn and assigns a set of coordinates to the list 'position' depending on the color of the pawn
            if self.color == "white":
                position = [(190, -3), (258, -3), (325, -3), (395, -3)]
            else:
                position = [(190, 583), (258, 583), (325, 583), (395, 583)]
        
            types = ["queen", "bishop", "knight", "rook"]
            all = []
            #creates the choices and appends them to the list 'all'
            for i in range(0, 4):
                all.append(choice(self.color, position[i], types[i]))
            
            #updates the display
            pygame.display.update() 

            #loop that runs until the user has selected a chess piece to promote the pawn to 
            promoted = False
            while not promoted:
                #calling the function 'mouse_up_down' which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
                event = mouse_up_down("down")
                #checking whether the 'MOUSEBUTTONDOWN' event collides with the rect of one of the choices
                for i in range(0, 4):
                    if all[i].rect.collidepoint(event.pos):
                        #changes the cursor to a diamond
                        pygame.mouse.set_cursor(pygame.cursors.diamond)
                        #calling the function 'mouse_up_down' which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
                        event2 = mouse_up_down("up")
                        found = False
                        #checking whether the 'MOUSEBUTTONUP' event collides with the rect of one of the choices
                        for i in range(0, 4):
                            if all[i].rect.collidepoint(event2.pos):
                                #changes the cursor to a arrow
                                pygame.mouse.set_cursor(pygame.cursors.arrow)

                                #erases the pawn from its position and moves its rect out of the screen
                                canvas.blit(background, chess_square.rect, chess_square.rect)
                                self.rect = self.rect.move(-1000, -1000)

                                #determines what type of chess_piece the piece selected is and creates it, placing it on the position the pawn was on
                                if all[i].type == "queen":
                                    chess_square.status = chess.queen(self.color, chess_square)
                                elif all[i].type == "bishop":
                                    chess_square.status = chess.bishop(self.color, chess_square)
                                elif all[i].type == "knight":
                                    chess_square.status = chess.knight(self.color, chess_square)
                                elif all[i].type == "rook": 
                                    chess_square.status = chess.rook(self.color, chess_square)

                                #erases the choices
                                for i in range(0, 4):
                                    canvas.blit(background, all[i].rect, all[i].rect)
                                
                                #updates the display   
                                pygame.display.update()

                                #sets promoted to True to end the loop 
                                promoted = True
                                found = True

                        #if the 'MOUSEBUTTONDOWN' event not found to collide with one of the choices' rect then the cursor is changed back to an arrow
                        if not found:
                            #changes the cursor to a arrow
                            pygame.mouse.set_cursor(pygame.cursors.arrow)
            
        #procedure that performs the enpassant movement by removing the pawn moved over
        def perform_enpassant(self, move):
            #finds the square the pawn moved over is on
            if self.color == "white":
                old_square = chessboard[move[0]][move[1]+1]
            else:
                old_square = chessboard[move[0]][move[1]-1]
            
            #updates the square the old pawn is on to "empty"
            old_pawn = old_square.status
            old_square.status == "empty"
            
            #erasing the old pawn and moving its rects out of the screen
            canvas.blit(background, old_square.rect, old_square.rect)
            old_pawn.rect = old_pawn.rect.move(-1000, -1000)
            old_pawn.rect_centre = old_pawn.rect_centre.move(-1000, -1000)

        #takes in the current square coordinates the pawn is in
        #returns the coordinates of the chessboard squares the pawn can move to
        def moves(self, x, y, special_moves):
            if self.color == "white":
                z = -1
            else:
                z = 1
            
            moves_unfiltered = [[x+1, y+z], [x, y+z], [x-1, y+z]]

            #checking whether the pawn has been moved before
            #if it hasn't, then add a 'forward by 2 squares' movement to the list moves_unfiltered
            if not self.moved:
                moves_unfiltered.append([x, y+z*2])

            moves = []
            
            for i in range (0, len(moves_unfiltered)):
                #checking whether the square coordinates are within the existing range of square coordinates
                if moves_unfiltered[i][0] >= 0 and moves_unfiltered[i][0] <= 7 and moves_unfiltered[i][1] >= 0 and moves_unfiltered[i][1] <= 7:
                    #filtering out the diagonal moves so that the pawn can be placed only on a diagonal block spot if there is another chess piece there
                    if chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status != "empty" and moves_unfiltered[i][0] != x:
                        moves.append(moves_unfiltered[i])
                        #checking whether there is a pawn on this spot
                        if isinstance(chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status, chess.pawn):
                            #checking whether the pawn has an enpassant status of "can be captured"
                            if chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status.enpassant == "can be captured":
                                #if so, the chessboard square coordinates of the square the pawn (on the diagonal spot) passed over are added to the 'moves' list
                                moves.append([moves_unfiltered[i][0], moves_unfiltered[i][1]+z])
                                #the coordinates are also added to the 'special_moves' list and identified as an en passant move
                                special_moves.append(["en passant", [moves_unfiltered[i][0], moves_unfiltered[i][1]+z]])
                    #filtering out the forward move so that a chess piece can only move forward if the chessboard square is empty
                    elif chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status == "empty" and moves_unfiltered[i][0] == x and moves_unfiltered[i][1] == y+z:
                        moves.append(moves_unfiltered[i])
                    #filtering out the 'forward by 2' move so that a chess piece can only move forward if the chessboard square it is moving to is empty and if the chessboard square it passes through is empty
                    elif chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status == "empty" and chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]-z].status == "empty"  and moves_unfiltered[i][0] == x and moves_unfiltered[i][1] == y+z*2:
                        moves.append(moves_unfiltered[i])
                        #adding the 'can be captured en passant' move to the 'special_moves' list
                        special_moves.append(["can be captured en passant", moves_unfiltered[i]])
                    #adding the diagonal moves with an empty spot to the 'special_moves' list, so that we can still record those spots as 'in_check' for the opposite color than that of the pawn
                    elif chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status == "empty" and moves_unfiltered[i][0] != x:
                        special_moves.append(["in check pawn", moves_unfiltered[i]])
            
            #checks whether the pawn would undergo promotion if moved to one of the places it can move to
            #if so, appends the chessboard square coordinates of the move along with the name of the special move (pawn promotion) to the global list 'special_moves'
            for i in range (0, len(moves)):
                if moves[i][1] == 7 and self.color == "black" or moves[i][1] == 0 and self.color == "white":
                    special_moves.append(["pawn promote", moves[i]])

            return moves, special_moves
            
#function that loads the chess pieces
def load_chess_piece(name):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, standard)
    return image

#function that returns the opposite color of a chess piece
def inverse(item):
    if item.color == "white":
        return "black"
    else:
        return "white"

#procedure that sets up the chess board
def set_up():
    colors = ["white", "black"]
    for x in range(0, 2):
        pos = [3, 4, 2, 1, 0, 5, 6, 7]
        if colors[x] == "white":
            y = 7
            z = 6
        else:
            y = 0
            z = 1
        chessboard[pos[1]][y].status = chess.king(colors[x], chessboard[pos[1]][y])
        #chessboard[pos[0]][y].status = chess.queen(colors[x], chessboard[pos[0]][y])
        j = 0
        for i in range (0,2):
            chessboard[pos[2+j]][y].status = chess.bishop(colors[x], chessboard[pos[2+j]][y])
            #chessboard[pos[3+j]][y].status = chess.knight(colors[x], chessboard[pos[3+j]][y])
            chessboard[pos[4+j]][y].status = chess.rook(colors[x], chessboard[pos[4+j]][y])
            j = 3
        j = 0
        for i in range (0, 8):
            #chessboard[j][z].status = chess.pawn(colors[x], chessboard[j][z])
            j += 1

#function that contains a loop that searches through the 2-D list of chessboard square until it finds the one that collides with the centre rect of the chess piece
#the loop will pick the first chessboard square selected in the list (in case the centre rect collides with more than one chessboard square)
#function returns the coordinates of the chessboard square the piece should be placed on
def find_square_coords(rect_x, rect_y):
    found_sqr = False
    i = -1
    j = 0
    while not found_sqr and j!= 8:
        i += 1
        if chessboard[i][j].rect.collidepoint(rect_x, rect_y):
            collision = [i, j]
            found_sqr = True
        if i == 7:
            i = -1
            j += 1  
    if found_sqr:
        return collision

#function that finds the chessboard square coordinates of the chess piece that is passed in
#returns the chessboard square coordinates
def find_piece(piece):
    for i in range (0, 8):
        for j in range(0, 8):
            if chessboard[i][j].status == piece:
                return i, j

#resets the selection
def reset_click(position, piece, event):
    #erases the place where the chess piece is, along with the highlight, and replaces it with an empty background 
    canvas.blit(background, position, position) 
    #replaces the image of the chess piece in the same position and moves the centre rect back to its old position
    canvas.blit(piece.img, position)
    piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+event.pos[0], -piece.rect_centre[1]+event.pos[1])

#function that checks whether the spot to be clicked on is valid
#returns boolean
def valid_move(available_moves, potential):
    valid = False
    for i in range (0, len(available_moves)):
        if available_moves[i][0] == potential[0] and available_moves[i][1] == potential[1]:
            valid = True
    return valid 

#main
canvas = create_screen()
background = load_background()
canvas.blit(background, (0, 0))  
standard = (70,70)      

#creating an array of all the squares, represented by rects, on the chess board
chessboard = []
for i in range (0, 8):
    chess_row = []
    for j in range(0, 8):
        chess_row.append(square(i, j))
    chessboard.append(chess_row)

#calling the procedure 'set_up' to set up the chess pieces and load the images onto the board
chess_pieces = []
set_up()

#sets each king object to a variable
blackking = chessboard[4][0].status  
whiteking = chessboard[4][7].status  

#creating the highlight rect that will be moved to select a chess piece
highlight = pygame.Rect((-100, -100), standard)

#setting the variable exit to False to start the loop
exit = False

#mainloop
while not exit:
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            found = False
            i = -1
            #looping through the list of chess pieces to identify whether a chess piece has been selected. 
            #the loop will pick the first chess piece selected in the list(in case the mouse click landed on two squares adjacent to each other)
            while not found and i != len(chess_pieces)-1:
                i += 1
                piece = chess_pieces[i]
                #sets 'special_moves' to []
                #this list will contain the special moves that could be performed on the chess piece from its current position
                special_moves = []
                
                #checks whether the piece has been selected
                if piece.rect.collidepoint(event.pos):
                    #selection of the chess piece
                    found = True
                    #changes the cursor to a diamond
                    pygame.mouse.set_cursor(pygame.cursors.diamond)

                    #calling the function 'mouse_up_down' which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
                    event_up = mouse_up_down("up")
                    pygame.mouse.set_cursor(pygame.cursors.arrow)
                    #moves and draws the highlight (to show that the piece has been selected)
                    highlight2 = highlight.move(piece.rect[0]+100, piece.rect[1]+100)
                    pygame.draw.rect(canvas, "gray", highlight2, 5)
                    #calls the function find_piece which finds the coordinates that the chessboard square that chess piece is on 
                    #then assigns the corresponding chessboard square to the variable 'chess_square_before'
                    chess_square_coords = find_piece(piece)
                    chess_square_before = chessboard[chess_square_coords[0]][chess_square_coords[1]]
                    #updates the display
                    pygame.display.update()

                    #selection and movement of the chess piece to the destination square

                    #checking whether the square pressed on is available for the chess piece to move to
                    #calling the function 'mouse_up_down' which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
                    event_down = mouse_up_down("down")
                    #moves the centre rect to the position the mousebutton has clicked down on
                    piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+event_down.pos[0], -piece.rect_centre[1]+event_down.pos[1])
                    #calls the function find_square to find which chessboard square this rect collides with
                    potential_x_y= find_square_coords(piece.rect_centre[0], piece.rect_centre[1])
                    #if it is within a square's region, and the square is within the possible moves of the piece, the cursor is changed to a diamond
                    if potential_x_y != None:
                        #the moves function is called (specific to the piece type) and the available moves that the piece can take are found as well as any special moves
                        available_moves_and_special_moves = piece.moves(chess_square_coords[0], chess_square_coords[1], special_moves)
                        special_moves = available_moves_and_special_moves[1]
                        
                        #calls the function check_check() which checks each movement of the piece and returns only the movements that would not result in the king (of the same color as the piece) being in check 
                        available_moves = chess.check_check(piece, chess_square_before, available_moves_and_special_moves[0])
                        
                        """add comments"""
                        if isinstance(piece, chess.king) or isinstance(piece, chess.rook):
                            if isinstance(piece, chess.king):
                                available_moves_and_special_moves = chess.king.add_castling(piece, chess_square_coords[0], chess_square_coords[1], available_moves, special_moves)
                            else:
                                available_moves_and_special_moves = chess.rook.add_castling(piece, chess_square_coords[0], chess_square_coords[1], available_moves, special_moves)
                            available_moves = available_moves_and_special_moves[0]
                            special_moves = available_moves_and_special_moves[1]

                        #calls function to check potential move validity
                        valid = valid_move(available_moves, potential_x_y)
                        #changes the cursor to a diamond if the potential move is valid
                        if valid:
                            pygame.mouse.set_cursor(pygame.cursors.diamond)

                    #moves the chess piece to the destination square (if the piece can be moved to it)
                    #this new square can be different than the square that the mouse was held down on in the previous section (in case the user changes their mind and clicks on a different square)
                    #calling the function 'mouse_up_down' which waits and checks for the event 'MOUSEBUTTONUP' or 'MOUSEBUTTONDOWN' depending on the argument passed in
                    event_up2 = mouse_up_down("up")
                    pygame.mouse.set_cursor(pygame.cursors.arrow)
                    #moves the centre rect to the new position. This will help figure out which square the chess piece should be put into
                    piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+event_up2.pos[0], -piece.rect_centre[1]+event_up2.pos[1])
                    #calls the function find_square which finds the chessboard square that the chess piece will be moved to 
                    potential_x_y_click = find_square_coords(piece.rect_centre[0], piece.rect_centre[1])
                    if potential_x_y_click != None:
                        #calls function to check move validity
                        valid = valid_move(available_moves, potential_x_y_click)
                        if valid:
                            chess_square = chessboard[potential_x_y_click[0]][potential_x_y_click[1]]
                            #checks whether the square is already occupied, and if so, erases the place where the piece was and moves its rect out of the screen
                            #this prevents the piece from appearing on the chessboard again
                            if chess_square.status != "empty":
                                chess_square.status.rect = chess_square.status.rect.move(-1000, -1000)
                                canvas.blit(background, chess_square.rect, chess_square.rect)
                                pygame.display.update()

                            #erases the place where the chess piece was, along with the highlight, and replaces it with an empty background 
                            canvas.blit(background, piece.rect, piece.rect) 
                            #moves the image of the chess piece to the new position, along with its rect and centre rect
                            canvas.blit(piece.img, chess_square.rect)
                            piece.rect = piece.rect.move(-piece.rect[0]+chess_square.rect[0], -piece.rect[1]+chess_square.rect[1])
                            piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+piece.rect[0]+35, -piece.rect_centre[1]+piece.rect[1]+35)
                            
                            #updates the display
                            pygame.display.update()   

                            #assigns the new chessboard square status to the chess piece
                            old_piece = chess_square.status
                            chess_square.status = piece

                            #sets the old chessboard square status to 'empty'
                            chess_square_before.status = "empty" 

                            #checks whether the new move is a special move
                            if special_moves != []:
                                found = False
                                a = -1

                                while not found and a <= len(special_moves)-2:
                                    a += 1
                                    if special_moves[a][1][0] == potential_x_y_click[0] and special_moves[a][1][1] == potential_x_y_click[1]:
                                        found = True
                                
                                if found:
                                    #checks whether the special move is a pawn promotion
                                    #if so, calls the subroutine promote() to promote the pawn 
                                    if special_moves[a][0] == "pawn promote":
                                        piece.promote(chess_square)

                                    #checks whether the special move is a castling move
                                    #if so, calls the subroutine castling() to perform the castling   
                                    if special_moves[a][0] == "castling":
                                        chess.castling(piece, special_moves[a], potential_x_y_click, old_piece)

                                    #checks whether the special move is an en passant move
                                    #if so, calls the subroutine perform_enpassant() to perform the en passant move
                                    if special_moves[a][0] == "en passant":
                                        piece.perform_enpassant(special_moves[a][1])

                                #resets any expired en passant possiblilities by setting the en passant status of the pawn to "no capture"
                                #an en passant move can only be carried out immediately after the pawn moves forward by 2 spaces; hence the expired en passant possibilites need to be removed
                                for c in range (0, 8):
                                    for d in range (0, 8):
                                        if isinstance(chessboard[c][d].status, chess.pawn):
                                            if chessboard[c][d].status.enpassant == "can be captured":
                                                chessboard[c][d].status.enpassant = "no capture"

                                #checks whether the special move found was a "can be captured en passant" flag
                                #if so, sets the en passant status of the pawn to "can be captured"
                                if found:
                                    if special_moves[a][0] == "can be captured en passant":
                                        piece.enpassant = "can be captured"

                            #sets the moved status of the chess piece to True
                            piece.moved = True 

                            #calls update_check() to update the 'in check' status of each chessboard square for both kings
                            chess.update_check()

                            #calls check_checkmate_stalemate() for each king to to check whether there is a checkmate or stalemate
                            chess.check_checkmate_stalemate(whiteking)
                            chess.check_checkmate_stalemate(blackking)

                        else:
                            #removes the selection
                            reset_click(piece.rect, piece, event)
                    else:
                        #removes the selection
                        reset_click(piece.rect, piece, event)

                    #updates the display
                    pygame.display.update()                
        #checking for the QUIT event and closing the window if needed 
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
