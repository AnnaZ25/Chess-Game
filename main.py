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

#class that contains the square blocks on the chessboard
class square:
    def __init__(self, x, y):
        #determines the position of the square on the chessboard and creates a rect to represent the square
        self.rect = pygame.Rect((x*65+63, y*65+63), standard)
        #determines the status of the square
        self.status = "empty"

#class that contains classes for each of the types of chess pieces
class chess:
    def __init__(self, color, square, type):
        self.color = color
        chess_pieces.append(self)
        position = square.rect
        #loading the object's image onto the board
        file_name = self.color + type + ".png"
        self.img = load_chess_piece(file_name)
        #creating a rect around the image and changing the position to match the image's position (needs to be scaled))
        canvas.blit(self.img, dest = position) 
        self.rect = self.img.get_rect(topleft = (position[0], position[1]))
        #creating a centre point so that the appropriate square the chess piece is moved to can be allocated accurately
        #this means that the chess piece can be made to sit exactly inside a square, even if not placed exactly inside the square by the user. 
        self.rect_centre = pygame.Rect(self.rect[0]+35, self.rect[1]+35, 1, 1)

    #function that finds the available moves of a piece from a list of possible moves
    def find_moves(self, moves):
        available_moves = []
        for i in range(0, len(moves)):
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
        return available_moves

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
            return chess.find_moves(self, moves)

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
            for i in range (-7, 8):
                moves.append([x+i, y-i])
                moves.append([x-i, y+i])
                moves.append([x+i, y+i])
                moves.append([x-i, y-i])
            for i in range (0, 4):
                moves.remove([x, y])
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
            for i in range (-7, 8):
                moves.append([x+i, y])
                moves.append([x, y+i])
            for i in range (0, 2):
                moves.remove([x, y])
            return chess.find_moves(self, moves)

    #class for the pawns
    class pawn:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "pawn")

        #takes in the current square coordinates the pawn is in
        #returns the coordinates of the chessboard squares the pawn can move to
        def moves(self, x, y):
            if self.color == "white":
                z = 1
            else:
                z = -1
            
            moves = [[x+1, y+z], [x, y+z], [x-1, y+z]]
            filtered = chess.find_moves(self, moves)
            moves = []
            #filtering out the diagonal moves so that the pawn can be placed only on a diagonal block spot if there is another chess piece there
            for i in range (0, len(filtered)):
                if chessboard[filtered[i][0]][filtered[i][1]].status != "empty" or filtered[i][0] == x:
                    moves.append(filtered[i])
            return moves
            
#function that loads the chess pieces
def load_chess_piece(name):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, standard)
    return image

#procedure that sets up the chess board
def set_up():
    colors = ["white", "black"]
    for x in range(0, 2):
        pos = [3, 4, 2, 1, 0, 5, 6, 7]
        if colors[x] == "white":
            y = 0
            z = 1
        else:
            y = 7
            z = 6
        chessboard[pos[0]][y].status = chess.king(colors[x], chessboard[pos[0]][y])
        chessboard[pos[1]][y].status = chess.queen(colors[x], chessboard[pos[1]][y])
        j = 0
        for i in range (0,2):
            chessboard[pos[2+j]][y].status = chess.bishop(colors[x], chessboard[pos[2+j]][y])
            chessboard[pos[3+j]][y].status = chess.knight(colors[x], chessboard[pos[3+j]][y])
            chessboard[pos[4+j]][y].status = chess.rook(colors[x], chessboard[pos[4+j]][y])
            j = 3
        j = 0
        for i in range (0, 8):
            chessboard[j][z].status = chess.pawn(colors[x], chessboard[j][z])
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
    #checking for the QUIT event and closing the window if needed 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            found = False
            i = -1
            #looping through the list of chess pieces to identify whether a chess piece has been selected. 
            #the loop will pick the first chess piece selected in the list(in case the mouse click landed on two squares adjacent to each other)
            while not found and i != len(chess_pieces)-1:
                i += 1
                piece = chess_pieces[i]
                #checks wether the piece has been selected
                if piece.rect.collidepoint(event.pos):
                    found = True
                    #changes the cursor to a diamond
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
                    received_up1 = False
                    #loop that runs until the mousebutton is up 
                    while not received_up1:
                        pygame.time.delay(10)
                        for event_up1 in pygame.event.get():
                            #checks for a 'mousebutton up' event
                            if event_up1.type == pygame.MOUSEBUTTONUP:
                                #sets the cursor to an arrow
                                pygame.mouse.set_cursor(pygame.cursors.arrow)
                                received_up1 = True
                                #moves and draws the highlight (to show that the piece has been selected)
                                highlight2 = highlight.move(piece.rect[0]+100, piece.rect[1]+100)
                                pygame.draw.rect(canvas, "gray", highlight2, 5)
                                #calls the function find_piece which finds the coordinates that the chessboard square that chess piece is on 
                                #then assigns the corresponding chessboard square to the variable 'chess_square_before'
                                chess_square_coords = find_piece(piece)
                                chess_square_before = chessboard[chess_square_coords[0]][chess_square_coords[1]]
                                #updates the display
                                pygame.display.update()
                                
                    received_down = False
                    while not received_down:
                        for event_down in pygame.event.get():
                            if event_down.type == pygame.MOUSEBUTTONDOWN:
                                received_down = True
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

                    recieved_up2 = False 
                    #loop that runs until the mousebutton is up (i.e. the user has selected a spot they want to put the chess piece in) 
                    while not recieved_up2:
                        pygame.time.delay(10)
                        position = piece.rect    
                        for event_up2 in pygame.event.get():
                            #checks for a 'mousebutton up' event
                            if event_up2.type == pygame.MOUSEBUTTONUP:
                                #sets the cursor to an arrow
                                pygame.mouse.set_cursor(pygame.cursors.arrow)
                                recieved_up2 = True
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
                                        canvas.blit(background, position, position) 
                                        #moves the image of the chess piece to the new position, along with its rect and centre rect
                                        canvas.blit(piece.img, chess_square.rect)
                                        piece.rect = piece.rect.move(-piece.rect[0]+chess_square.rect[0], -piece.rect[1]+chess_square.rect[1])
                                        piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+piece.rect[0]+35, -piece.rect_centre[1]+piece.rect[1]+35)
                                        
                                        #sets the old chessboard square status to 'empty'
                                        chess_square_before.status = "empty"   

                                        #assigns the new chessboard square status to the chess piece
                                        chess_square.status = piece

                                    else:
                                        #removes the selection
                                        reset_click(position, piece, event)
                                else:
                                    #removes the selection
                                    reset_click(position, piece, event)

                                #updates the display
                                pygame.display.update()                

        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
