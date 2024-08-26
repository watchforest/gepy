from .node import Node
from .edge import Edge

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y):
        node = Node(x, y)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen):
        for edge in self.edges:
            edge.draw(screen, WHITE)
        for node in self.nodes:
            node.draw(screen, WHITE)
