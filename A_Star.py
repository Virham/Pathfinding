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
        return abs(offset.x + offset.y)

    def getIndex(self):
        return int(self.pos.x + self.pos.y * self.pathfinder.width)

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

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                print(j, i)
                pos = pygame.Vector2(x + j * 2 - 1, y + i)
                if self.posInGrid(pos):
                    index = int(pos.x + pos.y * self.width)
                    print(index)
                    if self.nodes[index]:
                        neighbors.append(self.nodes[index])
                        continue
                    if self.cells[index]:
                        neighbors.append(Node(pos, self, current))

        return neighbors

    def solve(self):
        self.start = self.grid.IndexToCoord(self.grid.start)
        self.end = self.grid.IndexToCoord(self.grid.end)

        start_node = Node(self.start, self, None)
        end_node = Node(self.end, self, None)
        print(start_node.pos)
        self.saveNode(start_node)
        self.saveNode(end_node)

        open_nodes = {start_node}
        closed_nodes = set()

        while len(open_nodes):
            current = self.getCurrent(open_nodes)
            open_nodes.remove(current)
            closed_nodes.add(current)

            if current == end_node:
                return current

            current_index = current.getIndex()

            for neighbor in self.getNeighbors(current):
                print(not neighbor, neighbor in closed_nodes)
                print(closed_nodes)
                if not neighbor or neighbor in closed_nodes:
                    print(neighbor, "NEIGHBOR GONE")
                    continue

                neighbor_index = neighbor.getIndex()
                t_score = self.f_cost[current_index] + 1
                if t_score < self.f_cost[neighbor_index]:
                    self.f_cost[neighbor_index] = t_score
                    neighbor.parent = current
                print("GOT HERE")
                if neighbor not in open_nodes:
                    print("ADDING", neighbor)
                    open_nodes.add(neighbor)

        return "NO PATH"