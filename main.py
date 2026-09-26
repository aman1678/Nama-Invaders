import pygame as pg

class Bullet():
    """Handles a drawn cirle ("bullet") from player
    and its interactions"""

    def __init__(self, pos=None):
        self.pos = pg.Vector2(pos) if pos else pg.Vector2(0,0)

    def update(self, vel, dt):
        self.pos.y -= vel * dt

    


class Player():
    """Handles the player interactions such as shooting, taking
    damage, moving around, etc."""

    def __init__(self, screen, color):
        self.color = color
        self.health = 50
        self.pos = pg.Vector2(screen.get_width() * 0.5, 
                              screen.get_height() * 0.75)
        self.rect = pg.rect.Rect(self.pos.x, self.pos.y, 100, 30)
        self.bullet = Bullet(self.pos)

    def collision(self, bul):
        return pg.Rect.collidepoint(self.rect, bul)

    def motion(self, vel, dt, dir):
        dx, dy = 0, 0
        if dir == "x":
            dx = vel * dt
            self.pos.x += dx
        elif dir == "y":
            dy = vel * dt
            self.pos.y += dy
        pg.Rect.move_ip(self.rect, dx, dy)

class Alien():
    """Hanldes enemy interactions: motion, shooting, taking
    damage, etc."""

    def __init__(self, screen, vert):
        self.health = 50
        self.screen = screen
        self.vert = vert
        self.pos = pg.Vector2(self.screen.get_width() * 0.5, 
                              self.screen.get_height() * 0.1 + 50 * vert)
        self.rect = pg.rect.Rect(self.pos.x, self.pos.y, 100, 30)

    def collision(self, bul):
        return pg.Rect.collidepoint(self.rect, bul)
    
    def motion(self, v, dt, dir):
        dx = 0

        if dir == 1:
            dx = v * dt
        elif dir == 0:
            dx = -v * dt
        self.pos.x += dx * self.vert / 2
        pg.Rect.move_ip(self.rect, dx * self.vert / 2, 0)


# Game's main function
def main():

    # Setup
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Nama Invaders!")
    clock = pg.time.Clock()
    running = True
    dt = 0
    shoot = False  
    player = Player(screen, "white")
    aliens = []
    alien_dir = [1] * 3
    score = 0
    font = pg.font.Font(None, 36)

    for i in range(3):
        aliens.append(Alien(screen, i + 1))

    # Game's main loop
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")
        keys = pg.key.get_pressed()
        pg.draw.rect(screen, player.color, player.rect, 40)

        for alien in aliens:
            if alien.health > 0:
                pg.draw.rect(screen, "red", alien.rect, 40)

        # Player motion 
        if keys[pg.K_w]:
            player.motion(-300, dt, "y")
        if keys[pg.K_a]:
            player.motion(-300, dt, "x")
        if keys[pg.K_s]:
            player.motion(300, dt, "y")
        if keys[pg.K_d]:
            player.motion(300, dt,"x")

        # Bullet shooting
        if keys[pg.K_SPACE]:
            shoot = True
            player.bullet.pos.x = player.pos.x + 50
            player.bullet.pos.y = player.pos.y + 15

        # Bullet motion
        if shoot:
            pg.draw.circle(screen, "white", player.bullet.pos, 20)
            player.bullet.update(1000, dt)

        # Bullet goes offscreen
        if player.bullet.pos.y < 0:
            shoot = False

        # Motion for each alien
        for i, alien in enumerate(aliens):
            if alien.pos.x + 100 >= float(screen.get_width()):
                alien_dir[i] = 0
            elif alien.pos.x <= 0:
                alien_dir[i] = 1
            alien.motion(300, dt, alien_dir[i])

            if alien.health and alien.collision(player.bullet.pos) and shoot:
                shoot = False
                alien.health -= 10
                score += 10
                
        # Score 
        score_surface = font.render(f"Score {score}", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        screen.blit(score_surface, score_rect)
        
        pg.display.flip()
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == "__main__":
    main()
