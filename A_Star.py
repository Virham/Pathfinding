import collections
import math

import pygame


class Node:
    def __init__(self, pos, pathfinder, parent=None):
        self.pos = pos
        self.parent = parent
        self.pathfinder = pathfinder

    def calculateGCost(self):
        cost = 0
        node = self.parent
        while node:
            cost += 1
            node = node.parent
        return cost

    def calculateHCost(self):
        offset = (self.pos - self.pathfinder.end)
        return abs(offset.x) + abs(offset.y)

    def getIndex(self):
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

        self.cells = self.grid.activeCells
        self.width = self.grid.width
        self.height = self.grid.height
        self.size = self.width * self.height

        self.end = None
        self.start = None

        self.nodes = [None] * self.size
        self.f_cost = [math.inf] * self.size

    def getCurrent(self, open_nodes):
        getFCost = lambda x: self.f_cost[x.getIndex()]
        return min(open_nodes, key=getFCost)

    def saveNode(self, node):
        index = node.getIndex()
        self.nodes[index] = node
        self.f_cost[index] = node.calculateGCost() + node.calculateHCost()

    def posInGrid(self, pos):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def getNeighbors(self, current):
        x, y = current.pos
        neighbors = []

        for j, i in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            pos = pygame.Vector2(x + j, y + i)
            if self.posInGrid(pos):
                index = int(pos.x + pos.y * self.width)
                if self.nodes[index]:
                    neighbors.append(self.nodes[index])
                    continue
                if not self.cells[index]:
                    node = Node(pos, self, current)
                    neighbors.append(node)
                    self.saveNode(node)

        return neighbors

    def solve(self):
        self.start = self.grid.IndexToCoord(self.grid.start)
        self.end = self.grid.IndexToCoord(self.grid.end)

        start_node = Node(self.start, self, None)
        end_node = Node(self.end, self, None)
        self.saveNode(start_node)
        self.saveNode(end_node)

        open_nodes = {start_node}
        closed_nodes = set()

        while len(open_nodes):
            current = self.getCurrent(open_nodes)
            open_nodes.remove(current)
            closed_nodes.add(current)


            current_index = current.getIndex()

            for neighbor in self.getNeighbors(current):
                if neighbor == end_node:
                    neighbor.parent = current
                    return neighbor

                if not neighbor or neighbor in closed_nodes:
                    continue

                neighbor_index = neighbor.getIndex()
                t_score = self.f_cost[current_index] + 1
                if t_score < self.f_cost[neighbor_index]:
                    self.f_cost[neighbor_index] = t_score
                    neighbor.parent = current

                if neighbor not in open_nodes:
                    open_nodes.add(neighbor)

        return