import pygame

#function that loads the chess pieces
def load_chess_piece(name):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (70,70))
    return image

#new square allocation procedure for chess pieces
def position_piece(sqrx, sqry):
    init_sqr = 64
    next_sqr = 65
    position = (init_sqr + next_sqr*sqrx-1, init_sqr + next_sqr*sqry-1)
    return position

#class that contains classes for each of the types of chess pieces
class chess:
    def __init__(self, color, position, type):
            self.color = color
            chess_pieces.append(self)
         
            #loading the object's image onto the board
            file_name = self.color + type + ".png"
            self.img = load_chess_piece(file_name)
            canvas.blit(self.img, dest = position_piece(position[0], position[1])) 
            if color == "white":
                add = 60
            else:
                add = 30
            self.rect = self.img.get_rect(topleft = (position[0]*65+62, position[1]*70+add))
     

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

#initialising the window and configuring its details
pygame.init()
canvas = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Chess Game")
exit = False

img = pygame.image.load("blackking.png")
pygame.display.set_icon(img) 

image = pygame.image.load("chessboard.jpg")
image = pygame.transform.scale(image, (650,650))
 
canvas.blit(image, dest = (0,0))
#calling the procedure 'set_up' to set up the chess pieces and load the images onto the board
chess_pieces = []
set_up("white")
set_up("black")


#mainloop
while not exit:
    #checking for the QUIT event and closing the window if needed 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in chess_pieces:
               if piece.rect.collidepoint(event.pos):
                    print("On a piece")
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
