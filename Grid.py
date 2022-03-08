import pygame

class Grid:
    def __init__(self, main, startPos, width, height, pixelSize, outlineW):
        # POSITIONING
        self.startPos = startPos
        self.width = width
        self.height = height
        self.pixelSize = pixelSize
        self.outlineW = outlineW
        self.rect = pygame.Rect(self.startPos, pygame.Vector2(self.width, self.height) * self.pixelSize)

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
        self.ACTIVE_COLOR = (255, 0, 0)
        self.ACTIVE_HOVER_COLOR = (191, 63, 63)

        self.START_COLOR = (0, 0, 255)
        self.END_COLOR = (0, 255, 0)

    '''
        HELPER FUNCTIONS
    '''

    def InGrid(self, pos):
        xBound = self.startPos.x <= pos[0] <= self.startPos.x + self.width * self.pixelSize
        yBound = self.startPos.y <= pos[1] <= self.startPos.y + self.height * self.pixelSize
        return xBound and yBound

    def BrushInGrid(self, pos):
        '''
        checks all four corners to verify if any part is inside
        :param pos:
        :return bool:
        '''

        offset = self.brushSize * self.pixelSize
        corner1 = self.InGrid(pos)
        corner2 = self.InGrid((pos[0] + offset, pos[1]))
        corner3 = self.InGrid((pos[0], pos[1] + offset))
        corner4 = self.InGrid((pos[0] + offset, pos[1] + offset))
        return corner1 or corner2 or corner3 or corner4

    def InCoordGrid(self, pos):
        xBound = 0 <= pos[0] < self.width
        yBound = 0 <= pos[1] < self.height
        return xBound and yBound

    def CellInBrush(self, startPos):
        size = self.pixelSize * self.brushSize
        pos = self.OffsetBrushToMiddle(pygame.mouse.get_pos())
        return pygame.Rect((pos.x - self.pixelSize, pos.y - self.pixelSize), (size, size)).collidepoint(startPos)

    def PosToCoord(self, pos):
        x = (pos[0] - self.startPos[0]) // self.pixelSize
        y = (pos[1] - self.startPos[1]) // self.pixelSize
        return int(x), int(y)

    def PosToIndex(self, pos):
        x, y = self.PosToCoord(pos)
        return int(x + y * self.width)

    def IndexToPos(self, index):
        x = index % self.width
        y = (index - x) // self.width
        return self.startPos + pygame.Vector2(x * self.pixelSize, y * self.pixelSize)

    def IndexToCoord(self, index):
        return pygame.Vector2(self.PosToCoord(self.IndexToPos(index)))

    def OffsetBrushToMiddle(self, startPos):
        x = startPos[0] - (self.brushSize - 1) * self.pixelSize / 2
        y = startPos[1] - (self.brushSize - 1) * self.pixelSize / 2
        return pygame.Vector2(x, y)

    def ClosestCell(self, pos):
        xOffset = (pos[0] - self.startPos[0]) % self.pixelSize
        yOffset = (pos[1] - self.startPos[1]) % self.pixelSize
        return pygame.Vector2(pos[0] - xOffset, pos[1] - yOffset)

    def CellHover(self):
        pos = self.OffsetBrushToMiddle(pygame.mouse.get_pos())
        if not self.BrushInGrid(pos):
            return
        return self.ClosestCell(pos)

    '''
        FUNCTIONALITY FUNCTIONS
    '''

    def KeyPressed(self):
        keys = pygame.key.get_pressed()
        if not self.InGrid(pygame.mouse.get_pos()):
            return

        if keys[pygame.K_s]:
            self.start, self.end = self.SpecialPositions(self.start, self.end)

        if keys[pygame.K_e]:
            self.end, self.start = self.SpecialPositions(self.end, self.start)

    def SpecialPositions(self, special, other):
        pos = self.PosToIndex(pygame.mouse.get_pos())
        self.activeCells[pos] = False
        if pos == other:
            return pos, None
        if pos == special:
            return None, other
        return pos, other

    def ActivateCells(self, state):
        pos = self.OffsetBrushToMiddle(pygame.mouse.get_pos())
        x, y = self.PosToCoord(pos)
        if not self.BrushInGrid(pos):
            return

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                current_x = x + j
                current_y = y + i
                if not self.InCoordGrid((current_x, current_y)):
                    continue
                index = current_x + current_y * self.width
                self.activeCells[index] = state

    '''
        DRAW FUNCTIONS
    '''

    def DrawCellHover(self):
        active = self.CellHover()
        if not active:
            return

        for i in range(self.brushSize):
            for j in range(self.brushSize):
                start_pos = active + pygame.Vector2(j, i) * self.pixelSize
                if self.InGrid(start_pos + pygame.Vector2(self.pixelSize / 2)):
                    pygame.draw.rect(self.win, self.HOVER_COLOR, (start_pos, pygame.Vector2(self.pixelSize)))

    def DrawActiveCells(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.activeCells[j + i * self.width]:
                    startPos = self.startPos + pygame.Vector2(j * self.pixelSize, i * self.pixelSize)
                    color = self.ACTIVE_HOVER_COLOR if self.CellInBrush(startPos) else self.ACTIVE_COLOR

                    pygame.draw.rect(self.win, color, (startPos, (self.pixelSize, self.pixelSize)))

    def DrawSpecial(self):
        if self.start is not None:
            pygame.draw.rect(self.win, self.START_COLOR, (self.IndexToPos(self.start), pygame.Vector2(self.pixelSize)))
        if self.end is not None:
            pygame.draw.rect(self.win, self.END_COLOR, (self.IndexToPos(self.end), pygame.Vector2(self.pixelSize)))

    def DrawGrid(self):
        for i in range(self.width + 1):
            startPos = self.startPos + pygame.Vector2(i * self.pixelSize, 0)
            endPos = startPos + pygame.Vector2(0, self.height * self.pixelSize)
            pygame.draw.line(self.win, self.OUTLINE_COLOR, start_pos=startPos, end_pos=endPos, width=self.outlineW)

        for i in range(self.height + 1):
            startPos = self.startPos + pygame.Vector2(0, i * self.pixelSize)
            endPos = startPos + pygame.Vector2(self.width * self.pixelSize, 0)
            pygame.draw.line(self.win, self.OUTLINE_COLOR, start_pos=startPos, end_pos=endPos, width=self.outlineW)

    '''
        UPDATE FUNCTIONS
    '''

    def GridEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.KeyPressed()
            return
        if pygame.mouse.get_pressed()[0]:
            self.ActivateCells(True)
        if pygame.mouse.get_pressed()[2]:
            self.ActivateCells(False)
            return
        if event.type == pygame.MOUSEWHEEL:
            self.brushSize = max(min(self.brushSize + event.y, self.maxSize), self.minSize)
            return

    def Display(self):
        pygame.draw.rect(self.win, self.BACKGROUND_COLOR, self.rect)
        self.DrawCellHover()
        self.DrawActiveCells()
        self.DrawSpecial()
        self.DrawGrid()

