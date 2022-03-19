import pygame
from Grid import Grid
from A_Star import AStar


class Main:
    def __init__(self):
        self.winSize = (1280, 720)
        self.win = pygame.display.set_mode(self.winSize)
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.grid = Grid(main=self, 
                         start_pos=pygame.Vector2(25, 25),
                         width=50, height=40,
                         pixel_size=16, outline_width=1)

        self.algorithm = None
        self.visualizing = False

    def display(self):
        self.win.fill((225, 225, 225))
        self.grid.draw_background()

        if self.algorithm:
            self.algorithm.draw()

        self.grid.display()
        pygame.display.update()

    def calculate_path(self):
        algorithm = AStar(grid=self.grid)
        solved = algorithm.solve()
        if solved:
            self.algorithm = algorithm
            return

        self.algorithm = None

    def grid_changed(self):
        if self.visualizing:
            self.calculate_path()
            return

        self.algorithm = None

    def loop(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:  # Resets program
                        return
                    if keys[pygame.K_f]:
                        self.visualizing = not self.visualizing
                        self.grid_changed()

                changed = self.grid.event_handler(event)
                if changed:
                    self.grid_changed()

            self.display()
            self.clock.tick(self.FPS)


while True:
    Main().loop()
