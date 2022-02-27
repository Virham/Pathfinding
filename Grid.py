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

    def CellClicked(self, startPos):
        return self.InGrid(startPos) and pygame.Rect(startPos, (self.pixelSize, self.pixelSize)).collidepoint(pygame.mouse.get_pos())

    def PosToIndex(self, pos):
        x = (pos[0] - self.startPos[0]) // self.pixelSize
        y = (pos[1] - self.startPos[1]) // self.pixelSize
        return int(x + y * self.width)

    def IndexToPos(self, index):
        x = index % self.width
        y = (index - x) // self.width
        return self.startPos + pygame.Vector2(x * self.pixelSize, y * self.pixelSize)

    def ClosestCell(self, pos):
        xOffset = (pos[0] - self.startPos[0]) % self.pixelSize
        yOffset = (pos[1] - self.startPos[1]) % self.pixelSize
        return pygame.Vector2(pos[0] - xOffset, pos[1] - yOffset)

    def ACellActive(self):
        x, y = pygame.mouse.get_pos()
        if not self.rect.collidepoint(x, y):
            return
        return self.ClosestCell((x, y))

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
        print(pos)
        self.activeCells[pos] = False
        if pos == other:
            return pos, None
        if pos == special:
            return None, other
        return pos, other

    def ActivateCells(self, state):
        x, y = pygame.mouse.get_pos()
        if not self.rect.collidepoint(x, y):
            return
        index = self.PosToIndex((x, y))
        self.activeCells[index] = state

    '''
        DRAW FUNCTIONS
    '''

    def DrawCellHover(self):
        active = self.ACellActive()
        if not active:
            return
        pygame.draw.rect(self.win, self.HOVER_COLOR, (active, pygame.Vector2(self.pixelSize)))

    def DrawActiveCells(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.activeCells[j + i * self.width]:
                    startPos = self.startPos + pygame.Vector2(j * self.pixelSize, i * self.pixelSize)
                    color = self.ACTIVE_HOVER_COLOR if self.CellClicked(startPos) else self.ACTIVE_COLOR
                    pygame.draw.rect(self.win, color, (startPos,
                                                       (self.pixelSize, self.pixelSize)))

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

    def Display(self):
        pygame.draw.rect(self.win, self.BACKGROUND_COLOR, self.rect)
        self.DrawCellHover()
        self.DrawActiveCells()
        self.DrawSpecial()
        self.DrawGrid()

