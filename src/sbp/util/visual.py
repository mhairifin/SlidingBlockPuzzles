"""
Visualization script that uses pygame to show an animation of the 
puzzle being solved
"""

from sbp.genetic import *

class Visual():
    BLACK = 0,0,0
    WHITE = 255,255,255
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.board = puzzle.board.copy()
        self.length = len(puzzle.board.matrix)
        pygame.init()
        size = 700, 300
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(Visual.WHITE)
        pygame.display.flip()
        self.pieceIms = Visual.generateIms(puzzle.board.pieces)
        self.col = Visual.BLACK

    """
    Create buttons for puzzle solving and generation
    """
    def button(self, msg, x, y, w, h, colour, colourhover, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, colourhover,(x,y,w,h))
            if click[0]:
                action()
        else:
            pygame.draw.rect(self.screen, colour,(x,y,w,h))
        f = pygame.font.Font("freesansbold.ttf",20)
        textSurface = f.render(msg, True, Visual.BLACK)
        textRect = textSurface.get_rect()
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurface, textRect)

    def generateIms(pieces):
        ims = {}
        myfont = pygame.font.SysFont('Arial', 30)
        for id in pieces:
            color = np.random.choice(range(256), size=3)
            ims[id] = myfont.render(str(id), False, color)
        return ims

    def drawGoal(self):
        w,h = 40,40
        y = 50
        startx = self.length*w+3*y
        for i in range(self.length):
            x = startx
            for j in range(self.length):
                id = self.puzzle.goal[i][j]
                pygame.draw.rect(self.screen, Visual.BLACK, [x, y, w, h], 2)
                if id != 0:
                    self.screen.blit(self.pieceIms[id], (x+4,y+4))
                x += w
            y += h

    def drawBoard(self):
        w,h = 40,40
        y = 50
        for i in range(self.length):
            x = 50
            for j in range(self.length): 
                pygame.draw.rect(self.screen, self.col, [x, y, w, h], 2)
                x += w
            y += h

    def drawPieces(self):
        w,h = 40,40
        y = 50
        for i in range(self.length):
            x = 50
            for j in range(self.length):
                id = self.board.matrix[i][j]
                if id != 0:
                    self.screen.blit(self.pieceIms[id], (x+4,y+4))
                x += w
            y += h

    def drawState(self):
        self.screen.fill(Visual.WHITE)
        self.button("Solve Puzzle", 600, 100, 30, 20, pygame.Color('0x929591'), pygame.Color('0xd8dcd6'), works)
        self.button("Get puzzle", 600, 130, 30, 20, pygame.Color('0x929591'), pygame.Color('0xd8dcd6'), works)
        self.drawBoard()
        self.drawPieces()
        self.drawGoal()
        pygame.display.flip()

    def changeColor(self, color):
        self.col = color

"""
Runs animation visualisation
"""
def visualize(puzzle):
    vis = Visual(puzzle)
    GREEN = 0, 255, 0
    if messages:
        print("VISUAL")
        print("-----------------")

    start = pygame.time.get_ticks()
    i=0
    j=0
    done = False
    while not done:
        if i % 500000 == 0 and j<=puzzle.sol.solpos:
            move, vis.board, empty = SBP.domove(puzzle.sol.seq[j], vis.board)
            if messages:
                print(puzzle.sol.seq[j].describe)
            j+=1
            vis.drawState()
        elif j == puzzle.sol.solpos+1:
            vis.changeColor(GREEN)
            vis.drawState()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        i+=1
    pygame.quit()

"""
Visualise a still puzzle - deprecated by grid.py
"""
def basicVisualise(puzzle):
    vis = Visual(puzzle)
    stop = False
    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
        vis.drawState()
    pygame.quit()
