import math
import time
from GUI import *
import pygame


class Node:
    def __init__(self, pos, pathfinder, parent=None):
        self.pos = pos
        self.parent = parent
        self.pathfinder = pathfinder

    def direct_g_cost(self):
        cost = 0
        node = self.parent
        while node:
            cost += 1
            node = node.parent

        return cost - 1

    def direct_h_cost(self):
        offset = (self.pos - self.pathfinder.end_pos)
        return abs(offset.x) + abs(offset.y)

    def direct_f_cost(self):
        return self.direct_g_cost() + self.direct_h_cost()

    def get_index(self):
        return int(self.pos.x + self.pos.y * self.pathfinder.width)

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(str(self.pos))

    def __repr__(self):
        return f"pos: {self.pos} parent: {self.parent.pos if self.parent else None}"


class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.main = self.grid.main

        if grid.start is None or grid.end is None:
            return

        self.cells = self.grid.activeCells
        self.width = self.grid.width
        self.height = self.grid.height
        self.size = self.width * self.height
        self.gui = [Text(text="Current Length: 0", pos=(875, 150), size=50, max_width=350)]

        self.closed_colors = {}
        self.nodes = [None] * self.size
        self.f_cost = {i: math.inf for i in range(self.size)}

        self.end_pos = self.grid.index_to_coord(self.grid.end)
        self.end_node = self.create_node(self.end_pos)
        self.start_pos = self.grid.index_to_coord(self.grid.start)
        self.start_node = self.create_node(self.start_pos)

        self.open_nodes = {self.start_node}
        self.closed_nodes = set()
        self.path = None

        self.OPEN_COLOR = (64, 255, 64)
        self.CL_C_MIN = (255, 64, 64)
        self.CL_C_MAX = (255, 255, 64)

        self.visual_FPS = 4
        self.max_FPS = 60

    def reset(self):
        self.closed_colors = {}
        self.nodes = [None] * self.size
        self.f_cost = {i: math.inf for i in range(self.size)}

        self.end_pos = self.grid.index_to_coord(self.grid.end)
        self.end_node = self.create_node(self.end_pos)
        self.start_pos = self.grid.index_to_coord(self.grid.start)
        self.start_node = self.create_node(self.start_pos)

        self.open_nodes = {self.start_node}
        self.closed_nodes = set()
        self.path = None

    def get_current(self, open_nodes):
        return min(open_nodes, key=lambda x: self.f_cost[x.get_index()])

    def create_node(self, pos, parent=None):
        node = Node(pos, self, parent)
        self.save_node(node)
        return node

    def save_node(self, node):
        index = node.get_index()
        self.nodes[index] = node
        self.f_cost[index] = node.direct_f_cost()

    def pos_in_grid(self, pos):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def get_neighbors(self, current):
        x, y = current.pos
        neighbors = []

        for j, i in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            pos = pygame.Vector2(x + j, y + i)
            if self.pos_in_grid(pos):
                index = int(pos.x + pos.y * self.width)
                if self.nodes[index]:
                    neighbors.append(self.nodes[index])
                    continue
                if not self.cells[index]:
                    node = self.create_node(pos, current)
                    neighbors.append(node)

        return neighbors

    def do_iteration(self):
        current_node = self.get_current(self.open_nodes)
        current_index = current_node.get_index()

        # Current is now visited, can't be visited again
        self.open_nodes.remove(current_node)
        self.closed_nodes.add(current_node)

        for neighbor in self.get_neighbors(current_node):
            # reached the end, stop and return path
            if neighbor == self.end_node:
                neighbor.parent = current_node
                self.path = neighbor
                self.gui[0].text = f"Current length: {self.path.direct_g_cost()}"
                return

            # if the neighbor either outside grid or already been visited
            if not neighbor or neighbor in self.closed_nodes:
                continue

            # check if path to neighbor through current is better than current path
            neighbor_index = neighbor.get_index()
            t_score = self.f_cost[current_index] + 1

            if t_score < self.f_cost[neighbor_index]:
                self.f_cost[neighbor_index] = t_score
                neighbor.parent = current_node

            # if the neighbor has never been visited, add to choice
            if neighbor not in self.open_nodes:
                self.open_nodes.add(neighbor)

        self.path = current_node
        self.gui[0].text = f"Current length: {self.path.direct_g_cost()}"

    def calculate_closed_colors(self):
        min_f_cost = min(self.f_cost.values())
        max_f_cost = max(self.f_cost.values(), key=lambda x: x if x < math.inf else -1)
        f_cost_diff = max_f_cost - min_f_cost
        for node in self.closed_nodes:
            index = node.get_index()
            f_cost = self.f_cost[index]
            min_scale = (f_cost - min_f_cost) / f_cost_diff
            max_scale = 1 - min_scale

            r = self.CL_C_MIN[0] * min_scale + self.CL_C_MAX[0] * max_scale
            g = self.CL_C_MIN[1] * min_scale + self.CL_C_MAX[1] * max_scale
            b = self.CL_C_MIN[2] * min_scale + self.CL_C_MAX[2] * max_scale
            self.closed_colors[index] = (r, g, b)

    def draw(self):
        for node in self.open_nodes:
            self.grid.draw_node(node, self.OPEN_COLOR)

        for node in self.closed_nodes:
            index = node.get_index()
            self.grid.draw_node(node, self.closed_colors[index])

        self.grid.draw_path(self.path)

        for element in self.gui:
            element.draw(self.main.win)

    def visualize(self):
        if self.grid.start is None or self.grid.end is None:
            return

        while len(self.open_nodes):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.do_iteration()
            self.calculate_closed_colors()

            self.main.win.fill((200, 200, 200))
            self.main.draw_gui()
            self.grid.draw_background()
            self.grid.draw_walls(False)
            self.draw()
            self.grid.draw_special()
            pygame.display.update()

            if self.path == self.end_node:
                return

            time.sleep(1 / self.visual_FPS)
            self.visual_FPS = min(self.max_FPS, self.visual_FPS + 0.2)

    def solve(self):
        # no defined start or end
        if self.grid.start is None or self.grid.end is None:
            return

        while len(self.open_nodes):
            self.do_iteration()
            if self.path == self.end_node:
                self.calculate_closed_colors()
                return True

        # There is no path
        return
