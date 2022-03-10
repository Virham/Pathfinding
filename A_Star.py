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
        offset = (self.pos - self.pathfinder.end_pos)
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

        if not grid.start or not grid.end:
            print("RETURNING")
            return

        self.cells = self.grid.activeCells
        self.width = self.grid.width
        self.height = self.grid.height
        self.size = self.width * self.height

        self.nodes = [None] * self.size
        self.f_cost = [math.inf] * self.size

        self.end_pos = self.grid.IndexToCoord(self.grid.end)
        self.end_node = self.CreateNode(self.end_pos)
        self.start_pos = self.grid.IndexToCoord(self.grid.start)
        self.start_node = self.CreateNode(self.start_pos)

        self.open_nodes = {self.start_node}
        self.closed_nodes = set()

    def getCurrent(self, open_nodes):
        getFCost = lambda x: self.f_cost[x.getIndex()]
        return min(open_nodes, key=getFCost)

    def CreateNode(self, pos, parent=None):
        node = Node(pos, self, parent)
        self.saveNode(node)
        return node

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
                    node = self.CreateNode(pos, current)
                    neighbors.append(node)

        return neighbors

    def solve(self):
        # no defined start or end
        if not self.grid.start or not self.grid.end:
            return

        while len(self.open_nodes):
            current_node = self.getCurrent(self.open_nodes)
            current_index = current_node.getIndex()

            # Current is now visited, can't be visited again
            self.open_nodes.remove(current_node)
            self.closed_nodes.add(current_node)

            for neighbor in self.getNeighbors(current_node):
                # The neighbor is the end, stop and return path
                if neighbor == self.end_node:
                    neighbor.parent = current_node
                    return neighbor

                # if the neighbor either outside grid or already been visited
                if not neighbor or neighbor in self.closed_nodes:
                    continue

                # check if length of path to neighbor through current is better than current path
                neighbor_index = neighbor.getIndex()
                t_score = self.f_cost[current_index] + 1

                if t_score < self.f_cost[neighbor_index]:
                    self.f_cost[neighbor_index] = t_score
                    neighbor.parent = current_node

                # if the neighbor has never been visited, add to choice
                if neighbor not in self.open_nodes:
                    self.open_nodes.add(neighbor)

        # There is no path
        return
