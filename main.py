import pygame
import random
import math
import sys
import os
import asyncio  # Import necessário para Pygbag

WIDTH, HEIGHT = 1920, 1080
COLORS = [
    (255, 0, 0), (255, 127, 0), (255, 255, 0),
    (0, 255, 0), (0, 0, 255), (75, 0, 130),
    (148, 0, 211), (255, 20, 147), (0, 255, 255)
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eu te amuuh sempre, Alana ??")
clock = pygame.time.Clock()


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.color = random.choice(COLORS)
        self.speed = random.uniform(0.5, 2.5)
        self.angle = random.uniform(0, math.pi * 2)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.life = random.randint(60, 180)
        self.alpha = 255
        self.decay = random.uniform(1, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.alpha -= self.decay
        if self.alpha < 0:
            self.alpha = 0
        self.color = (*self.color[:3], int(self.alpha))

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color, (self.size, self.size), self.size)
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

    def is_dead(self):
        return self.life <= 0 or self.alpha <= 0


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=10)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class PhotoGallery:
    def __init__(self):
        self.photos = []
        self.current_photo = 0
        self.showing = False
        self.fade_alpha = 0
        self.fade_speed = 5
        self.message_font = pygame.font.Font(None, 48)
        self.message_text = "Alana você é meu sempre e eternamente Te amo mais que todas as estrelas Você é o amor da minha vida."
        self.message_alpha = 0
        self.message_y = HEIGHT - 100
        self.timer = 0
        self.auto_change_interval = 300
        self.load_photos()

    def load_photos(self):
        photo_folder = "fotos_alana"
        if self.try_load_real_photos(photo_folder):
            return
        self.create_sample_photos()

    def try_load_real_photos(self, folder_path):
        try:
            if not os.path.exists(folder_path):
                return False
            loaded_photos = False
            valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
            for filename in sorted(os.listdir(folder_path)):
                if filename.lower().endswith(valid_extensions):
                    try:
                        photo_path = os.path.join(folder_path, filename)
                        photo = pygame.image.load(photo_path).convert_alpha()
                        photo = pygame.transform.scale(photo, (1366, 768))
                        self.photos.append(photo)
                        loaded_photos = True
                    except Exception as e:
                        print(f"Erro ao carregar {filename}: {e}")
            return loaded_photos
        except Exception as e:
            print(f"Erro ao acessar a pasta: {e}")
            return False

    def create_sample_photos(self):
        sample_messages = self.message_text.split(',')
        for msg in sample_messages[:200]:
            photo = pygame.Surface((600, 400), pygame.SRCALPHA)
            for y in range(400):
                color = (
                    int(50 + y / 400 * 150),
                    int(50 + y / 400 * 100),
                    int(100 + y / 400 * 100)
                )
                pygame.draw.line(photo, color, (0, y), (600, y))
            font_large = pygame.font.Font(None, 50)
            text1 = font_large.render(msg.strip(), True, (255, 255, 255))
            text1_rect = text1.get_rect(center=(300, 150))
            photo.blit(text1, text1_rect)
            self.photos.append(photo)

    def update(self):
        if not self.showing:
            return
        if self.fade_alpha < 255:
            self.fade_alpha = min(self.fade_alpha + self.fade_speed, 255)
        self.timer += 1
        if self.timer % self.auto_change_interval == 0 and len(self.photos) > 1:
            self.next_photo()
        if self.timer % 2 == 0:
            self.message_y += math.sin(self.timer * 0.05) * 0.5
            if self.timer > 120:
                if self.message_alpha < 255 and self.timer < 300:
                    self.message_alpha = min(self.message_alpha + 3, 255)
                elif self.timer > 300:
                    self.message_alpha = max(self.message_alpha - 3, 0)

    def draw(self, surface):
        if not self.showing or not self.photos:
            return
        current_img = self.photos[self.current_photo]
        img_rect = current_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        surface.blit(current_img, img_rect)
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 255 - self.fade_alpha))
            surface.blit(fade_surface, (0, 0))
        if self.message_alpha > 0:
            text_surface = self.message_font.render(self.message_text.split(',')[0], True, (255, 255, 255))
            text_surface.set_alpha(self.message_alpha)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, self.message_y))
            surface.blit(text_surface, text_rect)
        if len(self.photos) > 1:
            indicator_font = pygame.font.Font(None, 30)
            indicator_text = f"{self.current_photo + 1}/{len(self.photos)}"
            indicator_surface = indicator_font.render(indicator_text, True, (255, 255, 255))
            indicator_rect = indicator_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            surface.blit(indicator_surface, indicator_rect)

    def show(self):
        self.showing = True
        self.fade_alpha = 0
        self.timer = 0
        self.message_alpha = 0
        self.current_photo = 0

    def next_photo(self):
        if len(self.photos) > 0:
            self.current_photo = (self.current_photo + 1) % len(self.photos)
            self.fade_alpha = 0
            self.timer = 0

    def prev_photo(self):
        if len(self.photos) > 0:
            self.current_photo = (self.current_photo - 1) % len(self.photos)
            self.fade_alpha = 0
            self.timer = 0

    def toggle(self):
        self.showing = not self.showing
        if self.showing:
            self.fade_alpha = 0
            self.message_alpha = 0
            self.timer = 0
            self.current_photo = 0


class FloatingText:
    def __init__(self, text, font_size, y_pos):
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.y_pos = y_pos
        self.x_pos = WIDTH // 2
        self.alpha = 0
        self.fade_in = True
        self.color = (255, 255, 255)
        self.shadow_color = (50, 50, 50)
        self.shadow_offset = 3
        self.angle = 0
        self.pulse_speed = 0.02

    def update(self):
        self.angle += self.pulse_speed
        if self.fade_in and self.alpha < 255:
            self.alpha += 3
            if self.alpha >= 255:
                self.alpha = 255
        r = int((math.sin(self.angle) * 0.5 + 0.5) * 255)
        g = int((math.sin(self.angle + math.pi / 1.5) * 0.5 + 0.5) * 255)
        b = int((math.sin(self.angle + 2 * math.pi / 1.5) * 0.5 + 0.5) * 255)
        self.color = (r, g, b)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        shadow_surface = self.font.render(self.text, True, self.shadow_color)
        shadow_surface.set_alpha(int(self.alpha * 0.7))
        text_rect = text_surface.get_rect(center=(self.x_pos, self.y_pos))
        shadow_rect = shadow_surface.get_rect(center=(self.x_pos + self.shadow_offset,
                                                      self.y_pos + self.shadow_offset))
        surface.blit(shadow_surface, shadow_rect)
        surface.blit(text_surface, text_rect)


class Heart:
    def __init__(self):
        self.particles = []
        self.timer = 0
        self.heartbeat = 0
        self.heart_size = 1.0
        self.heart_color = (255, 50, 50)

    def update(self):
        self.timer += 1
        self.heartbeat += 0.05
        self.heart_size = 1.0 + math.sin(self.heartbeat) * 0.1
        r = int((math.sin(self.heartbeat) * 127 + 128))
        g = int((math.sin(self.heartbeat + math.pi / 1.5) * 50 + 50))
        b = int((math.sin(self.heartbeat + 2 * math.pi / 1.5) * 50 + 50))
        self.heart_color = (r, g, b)

        if self.timer % 3 == 0:
            for _ in range(5):
                angle = random.uniform(0, math.pi * 2)
                radius = random.uniform(20, 50)
                x = WIDTH // 2 + math.cos(angle) * radius
                y = HEIGHT // 2 + math.sin(angle) * radius
                self.particles.append(Particle(x, y))

        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

        heart_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        points = []
        for t in range(0, 628, 5):
            t /= 100
            x = 16 * (math.sin(t) ** 3)
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            points.append((x * 10 * self.heart_size + 150, y * 10 * self.heart_size + 150))

        pygame.draw.polygon(heart_surf, (*self.heart_color, 200), points)

        for i in range(1, 4):
            glow_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
            pygame.draw.polygon(glow_surf, (*self.heart_color, 30 // i),
                                [(x + random.uniform(-i, i), y + random.uniform(-i, i)) for x, y in points])
            surface.blit(glow_surf, (WIDTH // 2 - 150, HEIGHT // 2 - 150))

        surface.blit(heart_surf, (WIDTH // 2 - 150, HEIGHT // 2 - 150))


class CinematicEffects:
    def __init__(self):
        self.lens_flare_pos = (-100, -100)
        self.lens_flare_timer = 0
        self.vignette_alpha = 0

    def update(self):
        self.lens_flare_timer += 1
        if self.lens_flare_timer % 100 == 0:
            self.lens_flare_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        if self.vignette_alpha < 100:
            self.vignette_alpha += 0.5

    def draw(self, surface):
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(vignette, (0, 0, 0, int(self.vignette_alpha)), (0, 0, WIDTH, HEIGHT))
        radius = min(WIDTH, HEIGHT) * 0.7
        pygame.draw.circle(vignette, (0, 0, 0, 0), (WIDTH // 2, HEIGHT // 2), int(radius))
        surface.blit(vignette, (0, 0))

        if random.random() < 0.02:
            flare = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(flare, (255, 255, 255, 50), (100, 100), 50)
            surface.blit(flare, (self.lens_flare_pos[0] - 100, self.lens_flare_pos[1] - 100))


async def main():
    heart = Heart()
    floating_text1 = FloatingText("Eu te amuuh Alana", 72, HEIGHT // 2 - 100)
    floating_text2 = FloatingText("Minha Princesa", 100, HEIGHT // 2 + 50)
    cinematic = CinematicEffects()
    gallery = PhotoGallery()
    button = Button(WIDTH - 220, HEIGHT - 70, 200, 50, "Nossas Memórias")

    floating_text1.fade_in = True
    floating_text2.fade_in = True

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif button.is_clicked(mouse_pos, event):
                gallery.toggle()

        heart.update()
        floating_text1.update()
        floating_text2.update()
        cinematic.update()
        gallery.update()
        button.check_hover(mouse_pos)

        for y in range(HEIGHT):
            color = (10, 0, int(10 + y / HEIGHT * 20))
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        heart.draw(screen)
        floating_text1.draw(screen)
        floating_text2.draw(screen)
        cinematic.draw(screen)
        gallery.draw(screen)
        button.draw(screen)

        if random.random() < 0.3:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice(COLORS)
            pygame.draw.circle(screen, (*color, 50), (x, y), random.randint(1, 3))

        pygame.display.flip()
        await asyncio.sleep(0)  # Pygbag precisa do async sleep

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
