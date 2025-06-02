import pygame, random, os, sys

# ————— Verificar carpeta de trabajo y contenido de images —————
BASE = os.path.abspath(os.path.dirname(__file__))
print("CARPETA DEL SCRIPT (BASE):", BASE)

images_folder = os.path.join(BASE, "images")
if os.path.isdir(images_folder):
    print("ARCHIVOS EN images/:", os.listdir(images_folder))
else:
    print("❌ NO existe la carpeta images/ en", BASE)

# ————— Inicialización de Pygame —————
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceMax Defender — Con Escudo (Ruta modificada)")
clock = pygame.time.Clock()

# ————— Colores y fuente —————
WHITE  = (255,255,255)
RED    = (220,20,60)
BLUE   = (50,150,255)
GREEN  = (50,200,50)
YELLOW = (255,200,0)
font   = pygame.font.Font(None, 36)

# ————— Función de carga con fallback y debug —————
def load_img(name, size, fallback_color):
    """
    Ahora busca en BASE/images/<name>. Si no existe, devuelve un rectángulo de color fallback_color.
    """
    path = os.path.join(BASE, 'images', name)
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
            print(f"✅ Cargó imagen: '{name}'  (ruta: {path})")
            return img
        except Exception as e:
            print(f"❌ Error al convertir '{name}': {e}")
    else:
        print(f"⚠️ NO encontró imagen: '{name}'")
        print(f"    Busqué en: {path}")
    # Placeholder visible si no la encuentra
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(fallback_color)
    return surf

# ————— Cargar sprites (nombres EXACTOS de los archivos en /images) —————
PLAYER_IMG = load_img('Tung.png',                        (60,  60), GREEN)
BOSS_IMG   = load_img('Bombardilo.png',                  (120,120), RED)
ENEMY_IMG  = load_img('BrrrPara-removebg-preview.png',   (40,  40), BLUE)

# ————— Fondo de estrellas —————
STARFIELD = pygame.Surface((WIDTH,HEIGHT))
STARFIELD.fill((0,0,0))
for _ in range(300):
    x,y = random.randrange(WIDTH), random.randrange(HEIGHT)
    pygame.draw.circle(STARFIELD, (200,200,255), (x,y), random.choice([1,2]))

# ————— Clases de efectos visuales —————
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, max_radius=30):
        super().__init__()
        self.pos = pos
        self.radius = 0
        self.max_radius = max_radius
        self.image = pygame.Surface((max_radius*2, max_radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
    def update(self):
        self.radius += 4
        if self.radius >= self.max_radius:
            self.kill()
            return
        self.image.fill((0,0,0,0))
        alpha = int(255 * (1 - self.radius/self.max_radius))
        pygame.draw.circle(
            self.image,
            (255,150,0,alpha),
            (self.max_radius, self.max_radius),
            self.radius
        )

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10,10), 10)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 3
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# ————— Sprites de juego —————
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect  = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-10))
        self.speed = 6
        self.lives = 3
        self.score = 0
        # Atributos de escudo
        self.shield_active = False
        self.shield_end = 0
        self.shield_cooldown = 0

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        # Movimiento izquierda/derecha
        if keys[pygame.K_LEFT]  and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        # Activar escudo con S
        if keys[pygame.K_s] and not self.shield_active and now >= self.shield_cooldown:
            self.shield_active = True
            self.shield_end = now + 3000         # dura 3 segundos
            self.shield_cooldown = now + 8000    # enfriamiento 8 segundos
            print("🛡️  Escudo ACTIVADO")
        # Desactivar escudo al expirar
        if self.shield_active and now >= self.shield_end:
            self.shield_active = False
            print("🛡️  Escudo DESACTIVADO")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, lv):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect  = self.image.get_rect(topleft=(x,y))
        self.speed = 2 + lv * 0.3
        self.dir   = 1
        self.shoot_delay = random.randint(max(20, 50 - lv*5), max(40, 80 - lv*5))
        self.tick = 0

    def update(self):
        self.rect.x += self.speed * self.dir
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.dir *= -1
            self.rect.y += 20
        self.tick += 1
        if self.tick >= self.shoot_delay:
            self.tick = 0
            b = EnemyBullet(self.rect.centerx, self.rect.bottom, 4)
            all_sprites.add(b)
            enemy_bullets.add(b)

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = BOSS_IMG
        self.rect  = self.image.get_rect(midtop=(WIDTH//2 - 60, 20))
        self.life  = 30
        self.dir   = 1
        self.speed = 3
        self.tick  = 0

    def update(self):
        self.rect.x += self.speed * self.dir
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dir *= -1
        self.tick += 1
        if self.tick >= 40:
            self.tick = 0
            # Disparo en abanico
            for angle in (-30, 0, 30):
                b = EnemyBullet(self.rect.centerx, self.rect.bottom, 6, angle)
                all_sprites.add(b)
                enemy_bullets.add(b)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(WHITE)
        self.rect  = self.image.get_rect(midbottom=(x,y))
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle=0):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(RED)
        self.rect  = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.vx = speed * (angle / 90)
        self.vy = speed

    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if (
            self.rect.top > HEIGHT or 
            self.rect.left < 0 or 
            self.rect.right > WIDTH
        ):
            self.kill()

# ————— Grupos de Sprites —————
all_sprites   = pygame.sprite.Group()
enemies       = pygame.sprite.Group()
bullets       = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
boss_group    = pygame.sprite.Group()
explosions    = pygame.sprite.Group()
powerups      = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# ————— Funciones de juego —————
def spawn_wave(lv):
    enemies.empty()
    for row in range(lv):
        for col in range(8):
            x = 60 + col * 80
            y = 60 + row * 60
            e = Enemy(x, y, lv)
            enemies.add(e)
            all_sprites.add(e)

def draw_hearts(n):
    for i in range(n):
        x0, y0 = 10 + i*35, 50
        pygame.draw.circle(screen, RED, (x0+8, y0+8), 8)
        pygame.draw.circle(screen, RED, (x0+20, y0+8), 8)
        pygame.draw.polygon(
            screen, RED,
            [(x0, y0+12), (x0+28, y0+12), (x0+14, y0+28)]
        )

# ————— Bucle principal —————
level = 1
spawn_wave(level)
running = True

while running:
    clock.tick(60)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            b = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(b)
            bullets.add(b)

    # Actualizar todos los sprites
    all_sprites.update()

    # Colisiones enemigos (niveles 1–3)
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for enemy in hits:
        player.score += 10 * level
        ex = Explosion(enemy.rect.center, max_radius=20 + level*3)
        all_sprites.add(ex)
        explosions.add(ex)
        if random.random() < 0.10:
            pu = PowerUp(enemy.rect.centerx, enemy.rect.centery)
            all_sprites.add(pu)
            powerups.add(pu)

    # Colisiones jefe (nivel 4)
    if level == 4 and boss_group:
        hitsB = pygame.sprite.groupcollide(boss_group, bullets, False, True)
        for _ in hitsB:
            boss.life -= 1
            ex = Explosion(boss.rect.center, 40)
            all_sprites.add(ex)
            explosions.add(ex)
            if boss.life <= 0:
                running = False

    # Colisiones jugador recibe bala (solo si no tiene escudo)
    if not player.shield_active:
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.lives -= 1
            ex = Explosion(player.rect.center, 30)
            all_sprites.add(ex)
            explosions.add(ex)
            if player.lives <= 0:
                running = False

    # Recoger PowerUps (+1 vida)
    for pu in pygame.sprite.spritecollide(player, powerups, True):
        player.lives = min(player.lives + 1, 5)

    # Avanzar de nivel
    if level < 4 and not enemies:
        level += 1
        spawn_wave(level)
        if level == 4:
            boss = Boss()
            all_sprites.add(boss)
            boss_group.add(boss)

    # Dibujar en pantalla
    screen.blit(STARFIELD, (0,0))
    all_sprites.draw(screen)

    # Dibujar escudo si está activo
    if player.shield_active:
        pygame.draw.circle(
            screen, BLUE,
            player.rect.center,
            player.rect.width//2 + 5,
            4
        )

    # HUD: Nivel y Score
    hud_text = f"Nivel: {level}   Score: {player.score}"
    screen.blit(font.render(hud_text, True, WHITE), (10,10))

    # Mostrar vidas
    draw_hearts(player.lives)

    # Barra de vida del jefe (si existe)
    if level == 4 and boss_group:
        pygame.draw.rect(screen, RED,    (WIDTH-220, 10, 210, 20))
        pygame.draw.rect(
            screen, (0,255,0),
            (WIDTH-220, 10, int(210 * boss.life / 30), 20)
        )

    pygame.display.flip()

pygame.quit()
sys.exit()

