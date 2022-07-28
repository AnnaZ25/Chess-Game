import pygame
  
pygame.init()
canvas = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Chess Game")
exit = False

img = pygame.image.load("blackking.png")
pygame.display.set_icon(img) 

image = pygame.image.load("chessboard.jpg")
image = pygame.transform.scale(image, (650,650))

def load_chess_piece(name):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (70,70))
    return image


def position_piece(sqrx, sqry):
    init_sqr = 64
    next_sqr = 65
    position = (init_sqr + next_sqr*sqrx-1, init_sqr + next_sqr*sqry-1)
    return position

class chess:
    def __init__(self, color, position):
            self.color = color
            self.position = position
            chess_pieces.append(self)

    def load_img(self, type):
        file_name = self.color + type + ".png"
        img = load_chess_piece(file_name)
        canvas.blit(img, dest = position_piece(self.position[0], self.position[1])) 

    class king:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "king")

    class queen:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "queen")
        
    class bishop:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "bishop")

    class knight:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "knight")

    class ruck:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "ruck")

    class pawn:
        def __init__(self, color, position):
            chess.__init__(self, color, position)
        
        def load(self):
            chess.load_img(self, "pawn")

    
canvas.blit(image, dest = (0,0))
chess_pieces = []


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
    

set_up("white")
set_up("black")

for item in chess_pieces:
    item.load()

while not exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
