import pygame


class Grid:
    def __init__(self, main, start_pos, width, height, pixel_size, outline_width):
        # POSITIONING
        self.start_pos = start_pos
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.outline_width = outline_width
        self.rect = pygame.Rect(self.start_pos, pygame.Vector2(self.width, self.height) * self.pixel_size)

        # API
        self.main = main
        self.win = main.win

        # GRID DATA
        self.activeCells = [False] * self.width * self.height
        self.start = None
        self.end = None

        # BRUSH CONFIG
        self.brushSize = 1
        self.minSize = 1
        self.maxSize = 10

        # COLORS
        self.OUTLINE_COLOR = (0, 0, 0)
        self.BACKGROUND_COLOR = (255, 255, 255)

        self.HOVER_COLOR = (127, 127, 127)
        self.ACTIVE_COLOR = (0, 0, 0)
        self.ACTIVE_HOVER_COLOR = (63, 63, 63)

        self.START_COLOR = (0, 0, 255)
        self.END_COLOR = (0, 255, 0)
        self.PATH_COLOR = (255, 0, 255)
        self.OPEN_COLOR = (64, 255, 64)
        self.CLOSED_COLOR = (255, 64, 64)

    """
        HELPER FUNCTIONS
    """

    def in_grid(self, pos):
        x_bound = self.start_pos.x <= pos[0] <= self.start_pos.x + self.width * self.pixel_size
        y_bound = self.start_pos.y <= pos[1] <= self.start_pos.y + self.height * self.pixel_size
        return x_bound and y_bound

    def brush_in_grid(self, pos):
        # checks all four corners to verify if any part is inside

        offset = self.brushSize * self.pixel_size
        corner1 = self.in_grid(pos)
        corner2 = self.in_grid((pos[0] + offset, pos[1]))
        corner3 = self.in_grid((pos[0], pos[1] + offset))
        corner4 = self.in_grid((pos[0] + offset, pos[1] + offset))
        return corner1 or corner2 or corner3 or corner4

    def in_coord_grid(self, pos):
        x_bound = 0 <= pos[0] < self.width
        y_bound = 0 <= pos[1] < self.height
        return x_bound and y_bound

    def cell_in_brush(self, start_pos):
        size = self.pixel_size * self.brushSize
        pos = self.offset_brush_to_middle(pygame.mouse.get_pos())
        return pygame.Rect((pos.x - self.pixel_size, pos.y - self.pixel_size), (size, size)).collidepoint(start_pos)

    def pos_to_coord(self, pos):
        x = (pos[0] - self.start_pos[0]) // self.pixel_size
        y = (pos[1] - self.start_pos[1]) // self.pixel_size
        return int(x), int(y)

    def coord_to_pos(self, coord):
        x = coord[0] * self.pixel_size + self.start_pos[0]
        y = coord[1] * self.pixel_size + self.start_pos[1]
        return pygame.Vector2(x, y)

    def pos_to_index(self, pos):
        x, y = self.pos_to_coord(pos)
        return int(x + y * self.width)

    def index_to_pos(self, index):
        x = index % self.width
        y = (index - x) // self.width
        return self.start_pos + pygame.Vector2(x * self.pixel_size, y * self.pixel_size)

    def index_to_coord(self, index):
        return pygame.Vector2(self.pos_to_coord(self.index_to_pos(index)))

    def offset_brush_to_middle(self, start_pos):
        x = start_pos[0] - (self.brushSize - 1) * self.pixel_size / 2
        y = start_pos[1] - (self.brushSize - 1) * self.pixel_size / 2
        return pygame.Vector2(x, y)

    def closet_cell(self, pos):
        x_offset = (pos[0] - self.start_pos[0]) % self.pixel_size
        y_offset = (pos[1] - self.start_pos[1]) % self.pixel_size
        return pygame.Vector2(pos[0] - x_offset, pos[1] - y_offset)

    def cell_hover(self):
        pos = self.offset_brush_to_middle(pygame.mouse.get_pos())
        if not self.brush_in_grid(pos):
            return
        return self.closet_cell(pos)

    """
        FUNCTIONALITY FUNCTIONS
    """

    def key_pressed(self):
        keys = pygame.key.get_pressed()
        if not self.in_grid(pygame.mouse.get_pos()):
            return

        if keys[pygame.K_s]:
            self.start, self.end = self.special_positions(self.start, self.end)

        if keys[pygame.K_e]:
            self.end, self.start = self.special_positions(self.end, self.start)

    def special_positions(self, special, other):
        pos = self.pos_to_index(pygame.mouse.get_pos())
        self.activeCells[pos] = False
        if pos == other:
            return pos, None
        if pos == special:
            return None, other
        return pos, other

    def activate_cells(self, state):
        pos = self.offset_brush_to_middle(pygame.mouse.get_pos())
        x, y = self.pos_to_coord(pos)
        if not self.brush_in_grid(pos):
            return

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                current_x = x + j
                current_y = y + i
                if not self.in_coord_grid((current_x, current_y)):
                    continue
                index = current_x + current_y * self.width
                self.activeCells[index] = state

    """
        DRAW FUNCTIONS
    """

    def draw_cell_hover(self):
        active = self.cell_hover()
        if not active:
            return

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                start_pos = active + pygame.Vector2(j, i) * self.pixel_size
                if self.in_grid(start_pos + pygame.Vector2(self.pixel_size / 2)):
                    pygame.draw.rect(self.win, self.HOVER_COLOR, (start_pos, pygame.Vector2(self.pixel_size)))

    def draw_active_cells(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.activeCells[j + i * self.width]:
                    start_pos = self.start_pos + pygame.Vector2(j * self.pixel_size, i * self.pixel_size)
                    color = self.ACTIVE_HOVER_COLOR if self.cell_in_brush(start_pos) else self.ACTIVE_COLOR

                    pygame.draw.rect(self.win, color, (start_pos, (self.pixel_size, self.pixel_size)))

    def draw_special(self):
        if self.start is not None:
            pygame.draw.rect(self.win, self.START_COLOR,
                             (self.index_to_pos(self.start), pygame.Vector2(self.pixel_size)))
        if self.end is not None:
            pygame.draw.rect(self.win, self.END_COLOR,
                             (self.index_to_pos(self.end), pygame.Vector2(self.pixel_size)))

    def draw_grid(self):
        for i in range(self.width + 1):
            start_pos = self.start_pos + pygame.Vector2(i * self.pixel_size, 0)
            end_pos = start_pos + pygame.Vector2(0, self.height * self.pixel_size)
            pygame.draw.line(self.win, self.OUTLINE_COLOR,
                             start_pos=start_pos, end_pos=end_pos, width=self.outline_width)

        for i in range(self.height + 1):
            start_pos = self.start_pos + pygame.Vector2(0, i * self.pixel_size)
            end_pos = start_pos + pygame.Vector2(self.width * self.pixel_size, 0)
            pygame.draw.line(self.win, self.OUTLINE_COLOR,
                             start_pos=start_pos, end_pos=end_pos, width=self.outline_width)

    def draw_path(self, path):
        if not path:
            return
        pygame.draw.rect(self.win, self.PATH_COLOR, (self.coord_to_pos(path.pos), pygame.Vector2(self.pixel_size)))
        self.draw_path(path.parent)

    def draw_open_nodes(self, open_nodes):
        for node in open_nodes:
            pygame.draw.rect(self.win, self.OPEN_COLOR,
                             (self.coord_to_pos(node.pos), pygame.Vector2(self.pixel_size)))

    def draw_closed_nodes(self, closed_nodes):
        for node in closed_nodes:
            pygame.draw.rect(self.win, self.CLOSED_COLOR,
                             (self.coord_to_pos(node.pos), pygame.Vector2(self.pixel_size)))

    """
        UPDATE FUNCTIONS
    """

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed()
            return "Changed"
        if pygame.mouse.get_pressed()[0]:
            self.activate_cells(True)
            return "Changed"
        if pygame.mouse.get_pressed()[2]:
            self.activate_cells(False)
            return "Changed"
        if event.type == pygame.MOUSEWHEEL:
            self.brushSize = max(min(self.brushSize + event.y, self.maxSize), self.minSize)
            return

    def draw_background(self):
        pygame.draw.rect(self.win, self.BACKGROUND_COLOR, self.rect)

    def display(self):
        self.draw_cell_hover()
        self.draw_active_cells()
        self.draw_special()
        self.draw_grid()
