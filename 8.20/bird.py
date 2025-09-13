import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids 群鸟模拟")

clock = pygame.time.Clock()

# ======== 参数 ========
SEPARATION_RADIUS = 25
SEPARATION_STRENGTH = 0.05
ALIGNMENT_RADIUS = 50
ALIGNMENT_STRENGTH = 0.05
COHESION_RADIUS = 50
COHESION_STRENGTH = 0.005
MAX_SPEED = 4
MOUSE_ATTRACT_STRENGTH = 0.0001  # ------- 新增：鼠标吸引力 ---------

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(
            random.uniform(0, WIDTH),
            random.uniform(0, HEIGHT)
        )
        self.velocity = pygame.Vector2(
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )

    def move(self):
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity

        # 地图环绕
        if self.position.x > WIDTH:
            self.position.x -= WIDTH
        if self.position.x < 0:
            self.position.x += WIDTH
        if self.position.y > HEIGHT:
            self.position.y -= HEIGHT
        if self.position.y < 0:
            self.position.y += HEIGHT

    def separation(self, boids):
        steer = pygame.Vector2(0, 0)
        count = 0
        for other in boids:
            if other is not self:
                dist = self.position.distance_to(other.position)
                if dist < SEPARATION_RADIUS and dist > 0:
                    diff = self.position - other.position
                    if dist != 0:
                        diff /= dist
                    steer += diff
                    count += 1
        if count > 0:
            steer /= count
            steer *= SEPARATION_STRENGTH
        return steer

    def alignment(self, boids):
        avg_vel = pygame.Vector2(0, 0)
        count = 0
        for other in boids:
            if other is not self:
                dist = self.position.distance_to(other.position)
                if dist < ALIGNMENT_RADIUS:
                    avg_vel += other.velocity
                    count += 1
        if count > 0:
            avg_vel /= count
            steer = (avg_vel - self.velocity) * ALIGNMENT_STRENGTH
            return steer
        else:
            return pygame.Vector2(0, 0)

    def cohesion(self, boids):
        avg_pos = pygame.Vector2(0, 0)
        count = 0
        for other in boids:
            if other is not self:
                dist = self.position.distance_to(other.position)
                if dist < COHESION_RADIUS:
                    avg_pos += other.position
                    count += 1
        if count > 0:
            avg_pos /= count
            direction = (avg_pos - self.position) * COHESION_STRENGTH
            return direction
        else:
            return pygame.Vector2(0, 0)

    # ------- 新增：鼠标吸引方法 -------
    def mouse_attract(self, mouse_target):
        if mouse_target is not None:
            # 鼠标吸引向量（指向鼠标点）
            direction = pygame.Vector2(mouse_target) - self.position
            return direction * MOUSE_ATTRACT_STRENGTH
        else:
            return pygame.Vector2(0, 0)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position.x), int(self.position.y)), 4)

NUM_BOIDS = 30
boids = [Boid() for _ in range(NUM_BOIDS)]

mouse_target = None  # ------- 新增：存鼠标点 -------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # ------- 新增：鼠标点击事件 -------
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_target = pygame.mouse.get_pos()

    screen.fill((0, 0, 0))

    for boid in boids:
        sep_force = boid.separation(boids)
        align_force = boid.alignment(boids)
        coh_force = boid.cohesion(boids)
        mouse_force = boid.mouse_attract(mouse_target)  # ------- 新增：鼠标力 -------

        boid.velocity += sep_force + align_force + coh_force + mouse_force
        boid.move()
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()