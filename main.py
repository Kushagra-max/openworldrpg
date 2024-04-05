import pygame
import os
import random

pygame.display.set_caption("Open World Test")

TILESIZE = 32
WIDTH = TILESIZE * 16
HEIGHT = TILESIZE * 12
PLAYER_SPEED = 3 * TILESIZE

# Define the camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)



        self.camera = pygame.Rect(x, y, self.width, self.height)

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.walk_buffer = 50
        self.pos = pygame.math.Vector2(x, y) * TILESIZE
        self.dirvec = pygame.math.Vector2(0, 0)
        self.last_pos = self.pos
        self.next_pos = self.pos
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.between_tiles = False
        
        # Load player image
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        # Load the player sprite image
        self.image = pygame.image.load("ethan.png").convert_alpha()  # Replace "player_sprite.png" with your sprite file path
        self.rect = self.image.get_rect(topleft = (self.pos.x, self.pos.y))

    def update(self, dt, walls):
        self.get_keys()
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        
        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > (self.dirvec * PLAYER_SPEED * dt).length():
                self.pos += self.dirvec * PLAYER_SPEED * dt
            else:
                self.pos = self.next_pos
                self.dirvec = pygame.math.Vector2(0, 0)
                self.between_tiles = False
                    
        self.rect.topleft = self.pos
        if pygame.sprite.spritecollide(self, walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.dirvec = pygame.math.Vector2(0, 0)
            self.between_tiles = False
        self.rect.topleft = self.pos

    def get_keys(self):        
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if now - self.last_update > self.walk_buffer:
            self.last_update = now
            
            new_dir_vec = pygame.math.Vector2(0, 0)
            if self.dirvec.y == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    new_dir_vec = pygame.math.Vector2(-1, 0)
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    new_dir_vec = pygame.math.Vector2(1, 0)
            if self.dirvec.x == 0:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    new_dir_vec = pygame.math.Vector2(0, -1)
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    new_dir_vec = pygame.math.Vector2(0, 1)
                
            if new_dir_vec != pygame.math.Vector2(0,0):
                self.dirvec = new_dir_vec
                self.between_tiles = True
                current_index = self.rect.centerx // TILESIZE, self.rect.centery // TILESIZE
                self.last_pos = pygame.math.Vector2(current_index) * TILESIZE
                self.next_pos = self.last_pos + self.dirvec * TILESIZE

# Define the obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((92, 64, 51))  # Brown obstacle
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))

# Load map from file
def load_map(folder, filename):
    file_path = os.path.join(folder, filename)
    with open(file_path, 'r') as file:
        map_data = [line.strip() for line in file.readlines()]
    return map_data

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load map files from folder
maps_folder = "maps"
map_files = [f for f in os.listdir(maps_folder) if f.endswith(".txt")]

# Check if map files exist
if not map_files:
    print("Error: No map files found in the 'maps' folder.")
    pygame.quit()
    exit()

# Randomly choose a map file
random_map_file = random.choice(map_files)
print(f"Loading map file: {random_map_file}")
try:
    MAP = load_map(maps_folder, random_map_file)
    print("Map loaded successfully.")
except Exception as e:
    print(f"Error loading map file '{random_map_file}': {e}")
    pygame.quit()
    exit()

# Initialize camera
camera = Camera(WIDTH, HEIGHT)

# Create sprite groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

# Create sprites from map data
for row, tiles in enumerate(MAP):
    for col, tile in enumerate(tiles):
        if tile == "1":
            obstacle = Obstacle(col, row)
            walls.add(obstacle)
            all_sprites.add(obstacle)
        elif tile == "P":
            player = Player(col, row)
            all_sprites.add(player)

# Main game loop
run = True
while run :
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update player
    player.update(dt, walls)

    # Update camera position to follow player
    camera.update(player)

    # Render game objects with camera offset
    window.fill((124, 252, 0))

    # Draw grid lines
    #for x in range(0, window.get_width(), TILESIZE):
     #   pygame.draw.line(window, (127, 127, 127), (x - camera.camera.x, 0), (x - camera.camera.x, window.get_height()))
    #for y in range(0, window.get_height(), TILESIZE):
     #   pygame.draw.line(window, (127, 127, 127), (0, y - camera.camera.y), (window.get_width(), y - camera.camera.y))

    # Apply camera offset to sprites
    for sprite in all_sprites:
        window.blit(sprite.image, camera.apply(sprite))

    pygame.display.flip()

pygame.quit()
exit()
