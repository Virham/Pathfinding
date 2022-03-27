import pygame

from GUI import Button
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

        self.gui = [Button(pos=(875, 32), width=350, height=100,
                           func=self.pathfinding,
                           text="Find Path", text_offset=pygame.Vector2(30, 0))]

    def draw_grid(self):
        self.grid.draw_background()

        if self.algorithm:
            self.algorithm.draw()

        self.grid.display()

    def draw_gui(self):
        for element in self.gui:
            element.draw(self.win)

    def display(self):
        self.win.fill((200, 200, 200))
        self.draw_grid()
        self.draw_gui()

        pygame.display.update()

    def calculate_path(self):
        algorithm = AStar(grid=self.grid)
        solved = algorithm.solve()
        if solved:
            self.algorithm = algorithm
            return

        self.visualizing = False
        self.algorithm = None

    def visualize_algorithm(self):
        algorithm = AStar(grid=self.grid)
        algorithm.visualize()

    def grid_changed(self):
        if self.visualizing:
            self.calculate_path()
            return

        self.algorithm = None

    def pathfinding(self):
        self.visualizing = not self.visualizing
        if self.visualizing:
            self.visualize_algorithm()
            self.calculate_path()
            return

        self.algorithm = None

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:  # Resets program
                return True

            if keys[pygame.K_f]:
                self.pathfinding()

        for element in self.gui:
            element.event_handler(event)

        changed = self.grid.event_handler(event)
        if changed:
            self.grid_changed()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if self.event_handler(event):  # if event handler returns back, restart game
                    return

            self.display()
            self.clock.tick(self.FPS)


while True:
    Main().loop()
