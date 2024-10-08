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

        self.BRUSH_COLOR = (127, 127, 127)
        self.ACTIVE_COLOR = (31, 31, 31)

        self.START_COLOR = (64, 64, 255)
        self.END_COLOR = (255, 64, 255)
        self.PATH_COLOR = (64, 255, 255)

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
            return True

        if keys[pygame.K_e]:
            self.end, self.start = self.special_positions(self.end, self.start)
            return True

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

        changed = False

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                current_x = x + j
                current_y = y + i
                if not self.in_coord_grid((current_x, current_y)):
                    continue
                index = current_x + current_y * self.width

                if not changed and self.activeCells[index] != state:
                    changed = True

                self.activeCells[index] = state

        return changed

    """
        DRAW FUNCTIONS
    """

    def draw_brush(self):
        start_pos = self.cell_hover()
        if not start_pos:
            return

        brush_surf = pygame.Surface(pygame.Vector2(self.brushSize * self.pixel_size))
        brush_surf.set_alpha(127)

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                pos = pygame.Vector2(j, i) * self.pixel_size
                if self.in_grid(start_pos + pos + pygame.Vector2(self.pixel_size / 2)):
                    pygame.draw.rect(brush_surf, self.BRUSH_COLOR, (pos, pygame.Vector2(self.pixel_size)))

        self.win.blit(brush_surf, start_pos)

    def draw_walls(self, show_active=True):
        for i in range(self.height):
            for j in range(self.width):
                if self.activeCells[j + i * self.width]:
                    start_pos = self.start_pos + pygame.Vector2(j * self.pixel_size, i * self.pixel_size)
                    pygame.draw.rect(self.win, self.ACTIVE_COLOR, (start_pos, (self.pixel_size, self.pixel_size)))

    def draw_special(self):
        if self.start is not None:
            pygame.draw.rect(self.win, self.START_COLOR,
                             (self.index_to_pos(self.start), pygame.Vector2(self.pixel_size)))
        if self.end is not None:
            pygame.draw.rect(self.win, self.END_COLOR,
                             (self.index_to_pos(self.end), pygame.Vector2(self.pixel_size)))

    def draw_background(self):
        pygame.draw.rect(self.win, self.BACKGROUND_COLOR, self.rect)

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
        self.draw_node(path, self.PATH_COLOR)
        self.draw_path(path.parent)

    def draw_node(self, node, color):
        pygame.draw.rect(self.win, color, (self.coord_to_pos(node.pos), pygame.Vector2(self.pixel_size)))

    """
        UPDATE FUNCTIONS
    """

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            return self.key_pressed()

        if event.type == pygame.MOUSEWHEEL:
            self.brushSize = max(min(self.brushSize + event.y, self.maxSize), self.minSize)

        if pygame.mouse.get_pressed()[0]:
            return self.activate_cells(True)

        if pygame.mouse.get_pressed()[2]:
            return self.activate_cells(False)

    def display(self):
        self.draw_walls()
        self.draw_special()
        self.draw_brush()
        # self.draw_grid()
