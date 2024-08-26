from .node import Node
from .edge import Edge

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, name, message):
        node = Node(x, y, name, message)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen, color):
        for edge in self.edges:
            edge.draw(screen, color)
        for node in self.nodes:
            node.draw(screen, color)


