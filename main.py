import pygame
import random

TILESIZE = 32
WIDTH = TILESIZE * 16
HEIGHT = TILESIZE * 12
PLAYER_SPEED = 3 * TILESIZE

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

tile_images = {
    '1': pygame.Surface((TILESIZE, TILESIZE)),
    'P': pygame.Surface((TILESIZE, TILESIZE)),
    # Add more tile images here as needed
}


MAP = ["1111111111111111",
       "1..............1",
       "1..............P",
       "1..1111........1",
       "1..1..1........1",
       "1..1111........1",
       "1..............1",
       "1........11111.1",
       "1........1...1.1",
       "1........11111.1",
       "1..............1",
       "1111111111111111"]

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
        
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (self.pos.x, self.pos.y))

    def update(self, dt, walls):
        self.get_keys()
        self.rect = self.image.get_rect(topleft = (self.pos.x, self.pos.y))
        
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
                
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((92, 64, 51))
        self.rect = self.image.get_rect(topleft = (x * TILESIZE, y * TILESIZE))

# Generate randmap map
def generate_random_map():
    new_map = []
    collison_tiles = 0
    max_collision_tiles = 5

    # generate map
    while collison_tiles < max_collision_tiles:
        new_map = []
        collison_tiles = 0

        for _ in range(12):
            row = ''.join(random.choice(['.', '.', '.', '.', '1']) for _ in range(16))
            collison_tiles += row.count('1')
            new_map.append(row)
    # Place player randomly in the new map
    random_row = random.randint(0, 11)
    random_col = random.randint(0, 15)
    new_map[random_row] = new_map[random_row][:random_col] + 'P' + new_map[random_row][random_col+1:]

    return new_map


MAP = generate_random_map()



#pygame.init()
#window = pygame.display.set_mode((WIDTH, HEIGHT))
#clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
for row, tiles in enumerate(MAP):
    for col, tile in enumerate(tiles):
        if tile == "1":
            obstacle = Obstacle(col, row)
            walls.add(obstacle)
            all_sprites.add(obstacle)
        elif tile == "P":
            player = Player(col, row)
            all_sprites.add(player)

# key presses and stuff           
run = True
while run :
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    player.update(dt, walls)

    # Check boundary touch
    if player.rect.left < 0 or player.rect.right > WIDTH or player.rect.top < 0 or player.rect.bottom > HEIGHT:
        # Generate a new random map
        MAP = generate_random_map()
        # Clear existing sprites
        all_sprites.empty()
        walls.empty()
        # Create new sprites for the new map
        for row, tiles in enumerate(MAP):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    obstacle = Obstacle(col, row)
                    walls.add(obstacle)
                    all_sprites.add(obstacle)
                elif tile == "P":
                    player = Player(col, row)
                    all_sprites.add(player)
    
    window.fill((124, 252, 0))

    for x in range (0, window.get_width(), TILESIZE):
        pygame.draw.line(window, (127, 127, 127), (x, 0), (x, window.get_height()))
    for y in range (0, window.get_height(), TILESIZE):
        pygame.draw.line(window, (127, 127, 127), (0, y), (window.get_width(), y))

    walls.draw(window)
    for sprite in all_sprites:
        window.blit(sprite.image, sprite.rect)


    pygame.display.flip()
    
pygame.quit()
exit()