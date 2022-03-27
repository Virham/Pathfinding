import pygame
pygame.init()


class Button:
    def __init__(self, pos, width, height, func, text, text_offset=(0, 0)):
        self.pos = pygame.Vector2(pos)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos, (self.width, self.height))

        self.func = func

        self.text = text
        self.text_offset = text_offset

        fitted_size = 2 * width / len(text)  # fits Impact font to width
        font_size = min(int(fitted_size), height - 10)
        self.font = pygame.font.SysFont("Impact", font_size)

    def draw(self, win):
        pygame.draw.rect(win, (64, 64, 64), (self.pos, (self.width, self.height)))
        rendered_text = self.font.render(self.text, False, (255, 255, 255))
        win.blit(rendered_text, self.pos + self.text_offset)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
            if mouse_rect.colliderect(self.rect):
                self.activated()

    def activated(self):
        self.func()


class Text:
    def __init__(self, text, pos, size, max_width=None, max_height=None):
        self.pos = pos
        self.size = size
        self.max_width = max_width
        self.max_height = max_height

        self.font = pygame.font.SysFont("Impact", self.size)
        self.text = text

        self.color = (255, 255, 255)

    def draw(self, win):
        render = self.font.render(self.text, False, self.color)
        win.blit(render, self.pos)

    def event_handler(self, event):
        pass
