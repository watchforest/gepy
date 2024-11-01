import pygame
import game.styles as colors
import time
import heapq

class Opponent(pygame.sprite.Sprite):
    def __init__(self, node, color, network):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(node.x, node.y))
        self.node = node
        self.target_node = node
        self.next_node = None
        self.speed = 5
        self.moving = False
        self.direction = pygame.math.Vector2(0, 0)
        self.active = False
        self.activation_delay = 1  # 1 second delay
        self.activation_start_time = None
        self.network = network
        self.path = []
        self.last_player_target = None

    def move_to_node(self, target_node):
        if target_node not in self.node.neighbors.values():
            print(f"Error: Attempting to move to non-adjacent node {target_node}")
            return
        self.target_node = target_node
        self.direction = pygame.math.Vector2(target_node.x - self.rect.centerx, target_node.y - self.rect.centery)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize() * self.speed
        self.moving = True

    def update(self, player, network):
        if not self.active:
            if self.activation_start_time is None:
                self.activation_start_time = time.time()
            elif time.time() - self.activation_start_time >= self.activation_delay:
                self.active = True
            return  # Don't update position if not active

        player_target = player.target_node if player.moving else player.node

        if not self.moving:
            if player_target != self.last_player_target:
                self.path = self.find_path(self.node, player_target)
                self.last_player_target = player_target
            if self.path:
                self.next_node = self.path.pop(0)
                self.move_to_node(self.next_node)
            else:
                self.next_node = None
        else:
            new_pos = self.rect.center + self.direction
            self.rect.center = new_pos
            to_target = pygame.math.Vector2(self.target_node.x - self.rect.centerx, self.target_node.y - self.rect.centery)
            if self.direction.dot(to_target) <= 0:
                self.rect.center = (self.target_node.x, self.target_node.y)
                self.node = self.target_node
                self.moving = False
                
                self.path = self.find_path(self.node, player_target)
                self.last_player_target = player_target
                
                if self.path:
                    self.next_node = self.path.pop(0)
                    self.move_to_node(self.next_node)
                else:
                    self.next_node = None

    def draw(self, surface, camera):
        if self.active:
            draw_pos = camera.apply(pygame.math.Vector2(self.rect.topleft))
            surface.blit(self.image, draw_pos)

    def start_activation_timer(self):
        self.activation_start_time = time.time()

    def find_path(self, start, goal):
        def heuristic(a, b):
            return pygame.math.Vector2(a.x - b.x, a.y - b.y).length()

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for next_node in current.neighbors.values():
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        return []  # No path found
