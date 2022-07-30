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

#class that contains classes for each of the types of chess pieces
class chess:
    def __init__(self, color, position, type):
            self.color = color
            chess_pieces.append(self)
         
            #loading the object's image onto the board
            file_name = self.color + type + ".png"
            self.img = load_chess_piece(file_name)
            canvas.blit(self.img, dest = position_piece(position[0], position[1])) 
            #creating a rectangle around the image and changing the position to match the image's position (needs to be scaled))
            self.rect = self.img.get_rect(topleft = (position[0]*65+63, position[1]*65+63))
     

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
def set_up(color):
    pos = [4, 3, 2, 1, 0, 5, 6, 7]
    if color == "white":
        y = 0
        z = 1
    else:
        y = 7
        z = 6

    chess.king(color, (pos[0], y))
    chess.queen(color, (pos[1], y))
    j = 0
    for i in range (0,2):
        chess.bishop(color, (pos[2+j],y))
        chess.knight(color, (pos[3+j],y))
        chess.ruck(color, (pos[4+j],y))
        j = 3
    j = 0
    for i in range (0, 8):
        chess.pawn(color, (j, z))
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

#calling the procedure 'set_up' to set up the chess pieces and load the images onto the board
chess_pieces = []
standard = (70,70)
set_up("white")
set_up("black")

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
                                #erases the place where the chess piece was, along with the highlight, and replaces it with an empty background 
                                canvas.blit(background, position, position)  
                                recieved_up2 = True
                                #moves the image of the chess piece to the new position, along with its rect
                                canvas.blit(piece.img, (event_up2.pos[0]-35, event_up2.pos[1]-35))
                                piece.rect = piece.rect.move(-piece.rect[0]+event_up2.pos[0]-35, -piece.rect[1]+event_up2.pos[1]-35)
                                #upates the display
                                pygame.display.update()                

        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
