import pygame
import random

# Inisialisasi Pygame
pygame.init()

# background
background_image = pygame.image.load("background.jpg")
background_width, background_height = background_image.get_rect().size
screen_width = background_width
screen_height = background_height

#setting screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Balok")

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Kelas untuk balok pemain
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2 
        self.rect.bottom = screen_height - 20
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        
        # tidak keluar layar
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0

# Kelas untuk enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

# group for all sprite
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Variabel untuk waktu
enemy_spawn_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

# Variabel poin 
points = 0

# Font
font = pygame.font.Font(None, 36)

# Loop utama
running = True
game_over = False
while running:
    # Tetap loop pada kecepatan frame yang tepat
    clock.tick(60)

    # Render gambar background
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cek skor
    if points >= 200 and not game_over:
        game_over = True  

    # Objek-objek game hanya akan diupdate jika game_over belum terjadi.
    if not game_over:
        all_sprites.update()

        # Spawn musuh
        now = pygame.time.get_ticks()
        if now - enemy_spawn_time > 2000:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_time = now

        # Collision detection
        hits = pygame.sprite.spritecollide(player, enemies, True)  # delete enemy 
        if hits:
            points += 10 
            # new enemy
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # render all screen
    all_sprites.draw(screen)

    # Tampilkan skor
    score_text = font.render("Score: {}".format(points), True, BLACK)
    screen.blit(score_text, (10, 10)) #kiri atas

    # Tampilkan pesan jika mencapai 50, 100, atau 200 koin
    if points >= 200:
        message_text = font.render("Selamat, kamu berhasil!", True, BLUE)
        screen.blit(message_text, (screen_width // 2 - 170, screen_height // 2 - 30))
    elif points == 50:
        message_text = font.render("Good Job!", True, BLUE)
        screen.blit(message_text, (screen_width // 2 - 80, screen_height // 2))
    elif points == 100:
        message_text = font.render("Waw Hebat!", True, BLUE)
        screen.blit(message_text, (screen_width // 2 - 90, screen_height // 2))

    pygame.display.flip()

pygame.quit()