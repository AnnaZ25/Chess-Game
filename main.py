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

    #class for the kings
    class king:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "king")

    #class for the queens
    class queen:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "queen")

    #class for the bishops   
    class bishop:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "bishop")

    #class for the knights
    class knight:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "knight")

    #class for the rucks
    class ruck:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "ruck")

    #class for the pawns
    class pawn:
        def __init__(self, color, position):
            chess.__init__(self, color, position, "pawn")

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
        chess.king(colors[x], chessboard[pos[0]][y])
        chess.queen(colors[x], chessboard[pos[1]][y])
        chessboard[pos[0]][y].status = colors[x]+"king"
        chessboard[pos[1]][y].status = colors[x]+"queen"
        j = 0
        for i in range (0,2):
            chess.bishop(colors[x], chessboard[pos[2+j]][y])
            chess.knight(colors[x], chessboard[pos[3+j]][y])
            chess.ruck(colors[x], chessboard[pos[4+j]][y])
            chessboard[pos[2+j]][y].status = colors[x]+"bishop"
            chessboard[pos[3+j]][y].status = colors[x]+"knight"
            chessboard[pos[4+j]][y].status = colors[x]+"ruck"
            j = 3
        j = 0
        for i in range (0, 8):
            chess.pawn(colors[x], chessboard[j][z])
            chessboard[j][z].status = colors[x]+"pawn"
            j += 1

#new square allocation procedure for chess pieces
def position_piece(sqrx, sqry):
    init_sqr = 64
    next_sqr = 65
    position = (init_sqr + next_sqr*sqrx-1, init_sqr + next_sqr*sqry-1)
    return position

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
            while not found and i != 31:
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
                                #updates the display
                                pygame.display.update()
            
                    recieved_up2 = False 
                    #loop that runs until the mousebutton is up (i.e. the user has selected a spot they want to put the chess piece in) 
                    while not recieved_up2:
                        pygame.time.delay(10)
                        position = piece.rect    
                        for event_up2 in pygame.event.get():
                            #checks for a 'mousebutton up' event
                            if event_up2.type == pygame.MOUSEBUTTONUP:
                                recieved_up2 = True
                                #moves the centre rect to the new position. This will help figure out which square the chess piece should be put into
                                piece.rect_centre = piece.rect_centre.move(-piece.rect_centre[0]+event_up2.pos[0], -piece.rect_centre[1]+event_up2.pos[1])
                                found_box = False
                                i = -1
                                j = 0
                                #loop that searches through the 2-D list of chessboard square until it finds the one that collides with the centre rect of the chess piece
                                #the loop will pick the first chessboard square selected in the list (in case the centre rect collides with more than one chessboard square)
                                while not found_box and j != 7:
                                    i += 1
                                    if chessboard[i][j].rect.collidepoint(piece.rect_centre[0], piece.rect_centre[1]):
                                        found_box = True
                                        #erases the place where the chess piece was, along with the highlight, and replaces it with an empty background 
                                        canvas.blit(background, position, position) 
                                        #moves the image of the chess piece to the new position, along with its rect and centre rect
                                        canvas.blit(piece.img, chessboard[i][j].rect)
                                        piece.rect = piece.rect.move(-piece.rect[0]+chessboard[i][j].rect[0], -piece.rect[1]+chessboard[i][j].rect[1])
                                        piece.rect_centre = piece.rect_centre.move(piece.rect[0]-35, piece.rect[1]-35)
                                    if i == 7:
                                        i = -1
                                        j += 1
                                #upates the display
                                pygame.display.update()                

        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
