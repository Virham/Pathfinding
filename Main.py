import pygame
from Grid import Grid
from A_Star import AStar


class Main:
    def __init__(self):
        self.winSize = (1280, 720)
        self.win = pygame.display.set_mode(self.winSize)
        self.grid = Grid(main=self, 
                         start_pos=pygame.Vector2(25, 25),
                         width=50, height=40,
                         pixel_size=16, outline_width=1)
        self.path = None
        self.open = None
        self.closed = None

        self.visualizing = False

    def display(self):
        self.win.fill((225, 225, 225))
        self.grid.draw_background()

        if self.path:
            self.grid.draw_open_nodes(self.open)
            self.grid.draw_closed_nodes(self.closed)
            self.grid.draw_path(self.path)

        self.grid.display()
        pygame.display.update()

    def visualize_path(self, algorithm):
        self.path = yield from algorithm.solve()

    def calculate_path(self):
        algorithm = AStar(grid=self.grid)
        path = algorithm.solve()
        if path:
            self.path, self.open, self.closed = path
            return

        self.clear_path()

    def clear_path(self):
        self.path = None
        self.open = None
        self.closed = None

    def grid_changed(self):
        if self.visualizing:
            self.calculate_path()
            return
        self.clear_path()

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

                state = self.grid.event_handler(event)
                if state:
                    self.grid_changed()

            self.display()


while True:
    Main().loop()
