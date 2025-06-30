import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # fallback; you can import from settings.py if preferred

class Bone:
    def __init__(self, name, length, timeline, angle=0, parent=None, image=None, image_path=None, offset=(0, 0)):
        self.name = name
        self.length = length
        self.angle = angle  # in degrees
        self.parent = parent
        self.image = image  # pygame.Surface or None
        self.image_path = image_path  # store the path string here for saving/loading
        self.offset = offset
        self.timeline = timeline
        self.children = []
        self.x = 0
        self.y = 0
        self.global_angle = 0
        if parent:
            parent.children.append(self)

    def update(self):
        if self.parent:
            px, py = self.parent.get_end()
            self.x, self.y = px, py
            self.global_angle = self.parent.global_angle + self.angle
        else:
            self.x = self.x or SCREEN_WIDTH // 2
            self.y = self.y or SCREEN_HEIGHT // 2
            self.global_angle = self.angle

        for child in self.children:
            child.update()

    def get_end(self):
        rad = math.radians(self.global_angle)
        ex = self.x + self.length * math.cos(rad)
        ey = self.y + self.length * math.sin(rad)
        return ex, ey

    def draw(self, surface, selected_bone):
        end_x, end_y = self.get_end()
        pygame.draw.line(surface, (255, 255, 0), (self.x, self.y), (end_x, end_y), 3)
        if self == selected_bone:
            pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), 7, 2)
        else:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 5)

        if self.image:
            rotated = pygame.transform.rotate(self.image, -self.global_angle)
            rect = rotated.get_rect()
            rect.center = (self.x, self.y)
            surface.blit(rotated, rect.topleft)

        for child in self.children:
            child.draw(surface, selected_bone)

        if self.name:
            font = pygame.font.SysFont(None, 18)
            angle_txt = font.render(f"{self.name}: {int(self.angle)}°", True, (255, 255, 255))
            surface.blit(angle_txt, (int(self.x + 10), int(self.y)))

    def is_clicked(self, mouse_pos, radius=10):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        return dx * dx + dy * dy <= radius * radius

    def look_at_mouse(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
