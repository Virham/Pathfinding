import pygame
from Grid import Grid
from A_Star import AStar

class Main:
    def __init__(self):
        self.winSize = (1280, 720)
        self.win = pygame.display.set_mode(self.winSize)
        self.grid = Grid(main=self, startPos=pygame.Vector2(25, 25), width=50, height=40, pixelSize=16, outlineW=1)
        self.pathfinding = AStar(grid=self.grid)

    def Display(self):
        self.win.fill((225, 225, 225))
        self.grid.Display()
        pygame.display.update()

    def Loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:  # Resets program
                    return
                if keys[pygame.K_f]:
                    print(self.pathfinding.solve())

                self.grid.GridEvent(event)

            self.Display()


while True:
    Main().Loop()
