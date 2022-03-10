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

    def display(self):
        self.win.fill((225, 225, 225))
        self.grid.display()

        if self.path:
            self.grid.draw_path(self.path)

        pygame.display.update()

    def print_path(self, node):
        if node:
            print(node)
            self.print_path(node.parent)

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
                        self.path = AStar(grid=self.grid).solve()

                self.grid.event_handler(event)
            self.display()


while True:
    Main().loop()
