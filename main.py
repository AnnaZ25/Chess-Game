#importing pygame
from numpy import asanyarray
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
    def find_moves(self, moves):
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
                    if chessboard_sqr.status.color != self.color and not isinstance(chessboard_sqr.status, chess.king):
                        available_moves.append(moves[i])
                else:
                    available_moves.append(moves[i])
            i += 1
        return available_moves

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

    #class for the kings
    class king:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "king")
            
        #takes in the current square coordinates the king is in
        #returns the coordinates of the chessboard squares the king can move to
        def moves(self, x, y):
            moves = []
            for i in range (-1, 2):
                for j in range (-1, 2):
                    moves.append([x+j, y+i])
            moves.remove([x, y])
            
            moves = chess.find_moves(self, moves)

            #checks whether the king has been moved before
            if self.moved == False:
                row = []
                for i in range(-4, 4):
                    row.append([x+i, y])
                #checks whether there is no chess piece between the king and the piece at the right end of the chessboard (also checks whether there is a piece at the last position of the row)
                if chessboard[row[5][0]][row[5][1]].status == "empty" and chessboard[row[6][0]][row[6][1]].status == "empty" and chessboard[row[7][0]][row[7][1]].status != "empty":
                    #checks whether the last piece is a rook and whether it has not been moved before
                    if isinstance(chessboard[row[7][0]][row[7][1]].status, chess.rook):
                        if not chessboard[row[7][0]][row[7][1]].status.moved:
                            #appends the chessboard square coordinates of the last piece and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                            special_moves.append(["castling", row[7], "r"])
                            #appends the chessboard square coordinates of the last piece to the list 'moves'
                            moves.append(row[7])
                #checks whether there is no chess piece between the king and the piece at the left end of the chessboard (also checks whether there is a piece at the first position of the row)
                if chessboard[row[2][0]][row[2][1]].status == "empty" and chessboard[row[2][0]][row[2][1]].status == "empty" and chessboard[row[3][0]][row[3][1]].status and chessboard[row[0][0]][row[0][1]].status != "empty":
                    #checks whether the first piece is a rook and whether it has not been moved before
                    if isinstance(chessboard[row[0][0]][row[0][1]].status, chess.rook):
                        if not chessboard[row[0][0]][row[0][1]].status.moved:
                            #appends the chessboard square coordinates of the first piece and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                            special_moves.append(["castling", row[0], "l"])
                            #appends the chessboard square coordinates of the first piece to the list 'moves'
                            moves.append(row[0])

            return moves

    #class for the queens
    class queen:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "queen")

        #takes in the current square coordinates the queen is in
        #returns the coordinates of the chessboard squares the queen can move to
        def moves(self, x, y):
            moves = []
            for i in range (-7, 8):
                moves.append([x+i, y])
                moves.append([x, y+i])
                moves.append([x+i, y-i])
                moves.append([x-i, y+i])
                moves.append([x+i, y+i])
                moves.append([x-i, y-i])
            for i in range (0, 6):
                moves.remove([x, y])
            return chess.find_moves(self, moves)

    #class for the bishops   
    class bishop:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "bishop")

        #takes in the current square coordinates the bishop is in
        #returns the coordinates of the chessboard squares the bishop can move to
        def moves(self, x, y):

            moves = []
            x_diag_raw = []
            minus_x_diag_raw = []
            for i in range (-7, 8):
                x_diag_raw.append([x-i, y+i])
                minus_x_diag_raw.append([x+i, y+i])
            
            
            def check(diag):
                diags = []
                for i in range (0, len(diag)):
                    if diag[i][0] >= 0 and diag[i][0] <= 7 and diag[i][1] >= 0 and diag[i][1] <= 7:
                        diags.append(diag[i])
                return diags

            x_diag = check(x_diag_raw)
            minus_x_diag = check(minus_x_diag_raw)


            print(x_diag)
            print(minus_x_diag)
            for i in range (0, len(x_diag)):
                pygame.draw.rect(canvas, "blue", chessboard[x_diag[i][0]][x_diag[i][1]], 3)
            for i in range (0, len(minus_x_diag)):
                pygame.draw.rect(canvas, "blue", chessboard[minus_x_diag[i][0]][minus_x_diag[i][1]], 3)    


            def find_bishop_movements(moves, row_col):
                moves1 = []
                empty_found = False
                i = len(row_col) - 1
                while i > -1 and not empty_found:
                    moves1.append(row_col[i])
                    if chessboard[row_col[i][0]][row_col[i][1]].status != "empty":
                        empty_found = True
                    i -= 1

                moves2 = []
                empty_found = False
                i = 0
                while i < len(row_col) and not empty_found:
                    moves2.append(row_col[i])
                    if chessboard[row_col[i][0]][row_col[i][1]].status != "empty":
                        empty_found = True
                    i += 1

                #print(moves1)
                #print(moves2)
                for i in range (0, len(moves1)):
                    moves.append(moves1[i])
                for i in range (0, len(moves2)):
                    moves.append(moves2[i])

                return moves

            coords = [find_piece(self)[0], find_piece(self)[1]]
            i = 0
            length = len(x_diag)
            while i < length:
                if x_diag[i] == coords:
                    x_diag.remove(x_diag[i])
                    length = len(x_diag)
                i += 1

            i = 0
            length = len(minus_x_diag)
            while i < length:
                if minus_x_diag[i] == coords:
                    minus_x_diag.remove(minus_x_diag[i])
                    length = len(minus_x_diag)
                i += 1

            moves = find_bishop_movements(moves, x_diag)
            moves = find_bishop_movements(moves, minus_x_diag)
            print("\n")

            return chess.find_moves(self, moves)
            

    #class for the knights
    class knight:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "knight")

        #takes in the current square coordinates the knight is in
        #returns the coordinates of the chessboard squares the knight can move to
        def moves(self, x, y):
            moves = []
            for i in range (-2, 0):
                moves.append([x+i, y+3+i]) 
                moves.append([x-i, y-3-i])
            moves.append([x+1, y+2])
            moves.append([x+2, y+1])
            moves.append([x-2, y-1])
            moves.append([x-1, y-2])
            return chess.find_moves(self, moves)

    #class for the rooks
    class rook:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "rook")
        
        #takes in the current square coordinates the rook is in
        #returns the coordinates of the chessboard squares the rook can move to
        def moves(self, x, y): 
            moves = []
            row = []
            col = []
            for i in range (0, 8):
                row.append([i, y])
                col.append([x, i])

            def find_rook_movements(moves, row_col, coor):
                moves1 = []
                empty_found = False
                i = 7
                while i > -1 and not empty_found:
                    moves1.append(row_col[i])
                    if chessboard[row_col[i][0]][row_col[i][1]].status != "empty" and i < coor:
                        empty_found = True
                    i -= 1

                moves2 = []
                empty_found = False
                i = 0
                while i < 8 and not empty_found:
                    moves2.append(row_col[i])
                    if chessboard[row_col[i][0]][row_col[i][1]].status != "empty" and i > coor:
                        empty_found = True
                    i += 1

                for i in range (0, len(moves1)):
                    for j in range (0, len(moves2)):
                        if moves1[i] == moves2[j]:
                            moves.append(moves1[i])

                return moves

            moves = find_rook_movements(moves, row, x)
            moves = find_rook_movements(moves, col, y)
            moves = chess.find_moves(self, moves)

            #checks whether the rook has been moved before
            if self.moved == False:
                #checks whether the rook is the last one in the row, or the first one in the row
                if x == 7:
                    #checks whether there is no chess piece between the rook and the piece on the 4th position of the chessboard row (also checks whether there is a piece at this position)
                    if chessboard[6][y].status == "empty" and chessboard[5][y].status == "empty" and chessboard[4][y].status != "empty":
                        #checks whether the piece on the 4th position of the chessboard row is a  is a king and whether it has not been moved before
                        if isinstance(chessboard[4][y].status, chess.king):
                            if not chessboard[4][y].status.moved:
                                #appends the chessboard square coordinates of the king and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                                special_moves.append(["castling", [4, y], "r"])
                                #appends the chessboard square coordinates of the king to the list 'moves'
                                moves.append([4, y])
                elif x == 0:
                    #checks whether there is no chess piece between the rook and the piece on the 4th position of the chessboard row (also checks whether there is a piece at this position)
                    if chessboard[1][y].status == "empty" and chessboard[2][y].status == "empty" and chessboard[3][y].status and chessboard[4][y].status != "empty":
                        #checks whether the piece on the 4th position of the chessboard row is a king and whether it has not been moved before
                        if isinstance(chessboard[4][y].status, chess.king):
                            if not chessboard[4][y].status.moved:
                                #appends the chessboard square coordinates of the king and the name of the special movement along with the identification of the side of the chessboard to the list 'special_moves'
                                special_moves.append(["castling", [4, y], "l"])
                                #appends the chessboard square coordinates of the king to the list 'moves'
                                moves.append([4, y])
            return moves
        
    #class for the pawns
    class pawn:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "pawn")
            self.moved = False

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
            
        #takes in the current square coordinates the pawn is in
        #returns the coordinates of the chessboard squares the pawn can move to
        def moves(self, x, y):
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
            #filtering out the diagonal moves so that the pawn can be placed only on a diagonal block spot if there is another chess piece there
            #filtering out the forward move so that a chess piece can only move forward if the chessboard square is empty
            for i in range (0, len(moves_unfiltered)):
                #checking whether the square coordinates are within the existing range of square coordinates
                if moves_unfiltered[i][0] >= 0 and moves_unfiltered[i][0] <= 7 and moves_unfiltered[i][1] >= 0 and moves_unfiltered[i][1] <= 7:
                    if chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status != "empty" and moves_unfiltered[i][0] != x:
                        moves.append(moves_unfiltered[i])
                    elif chessboard[moves_unfiltered[i][0]][moves_unfiltered[i][1]].status == "empty" and moves_unfiltered[i][0] == x:
                        moves.append(moves_unfiltered[i])
            
            #checks whether the pawn would undergo promotion if moved to one of the places it can move to
            #if so, appends the chessboard square coordinates of the move along with the name of the special move (pawn promotion) to the global list 'special_moves'
            for i in range (0, len(moves)):
                if moves[i][1] == 7 and self.color == "black" or moves[i][1] == 0 and self.color == "white":
                    special_moves.append(["pawn promote", moves[i]])

            return moves
            
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
            chessboard[pos[3+j]][y].status = chess.knight(colors[x], chessboard[pos[3+j]][y])
            #chessboard[pos[4+j]][y].status = chess.rook(colors[x], chessboard[pos[4+j]][y])
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
                        #the moves function is called (specific to the piece type) and the available moves that the piece can take are found
                        available_moves = piece.moves(chess_square_coords[0], chess_square_coords[1])
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
                                i = -1
                                while not found and i <= len(special_moves)-2:
                                    i += 1
                                    if special_moves[i][1][0] == potential_x_y_click[0] and special_moves[i][1][1] == potential_x_y_click[1]:
                                        found = True
                                
                                if found:
                                    #checks whether the special move is a pawn promotion
                                    #if so, calls the subroutine promote() to promote the pawn 
                                    if special_moves[i][0] == "pawn promote":
                                        piece.promote(chess_square)
                                    #checks whether the special move is a castling move
                                    #if so, calls the subroutine castling() to perform the castling   
                                    if special_moves[i][0] == "castling":
                                        chess.castling(piece, special_moves[i], potential_x_y_click, old_piece)
                                
                            piece.moved = True 


                            """
                            def remove_castling(available_moves, a, b):
                                to_remove = []
                                if isinstance(chessboard[a][b].status, chess.king) and chessboard[a][b].status.moved == False:
                                    for i in range(0, len(available_moves)):
                                        if available_moves[i] == [7, b]:
                                            to_remove.append([7, b])
                                        elif available_moves[i] == [0, b]:
                                            to_remove.append([0, b])
                                    for i in range (0, len(to_remove)):
                                        available_moves.remove(to_remove[i])
                                return available_moves

                            for a in range (0, len(chessboard)):
                                for b in range(0, len(chessboard)):
                                    if chessboard[a][b].status != "empty":
                                        if chessboard[a][b].status.color == "white":
                                            available_moves = chessboard[a][b].status.moves(a, b) 
                                            available_moves = remove_castling(available_moves, a, b)
                                            for k in range(0, len(available_moves)):
                                                chessboard[available_moves[k][0]][available_moves[k][1]].sqr_in_check_black = True
                                        elif chessboard[a][b].status.color == "black":
                                            available_moves = chessboard[a][b].status.moves(a, b) 
                                            available_moves = remove_castling(available_moves, a, b)
                                            for k in range(0, len(available_moves)):
                                                chessboard[available_moves[k][0]][available_moves[k][1]].sqr_in_check_white = True
                            
                            for a in range(0, len(chessboard)):
                                for b in range (0, len(chessboard)):
                                    if chessboard[b][a].sqr_in_check_white:
                                        #pygame.draw.rect(canvas, "gray", chessboard[b][a].rect, 10)
                              """  


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