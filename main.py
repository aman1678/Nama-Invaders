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
        self.pos = pg.Vector2(screen.get_width() * 0.5, 
                              screen.get_height() * 0.75)
        self.rect = pg.rect.Rect(self.pos.x, self.pos.y, 100, 30)

    def collision(self, enemy_bullet):
        return pg.Rect.collidepoint(enemy_bullet)

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
    bullet = Bullet()
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
                pg.draw.rect(screen, "white", alien.rect, 40)

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
            bullet = Bullet(player.pos)
            bullet.pos.x = player.pos.x + 50
            bullet.pos.y = player.pos.y - 15
            shoot = True

        # Bullet motion
        if shoot:
            pg.draw.circle(screen, "white", bullet.pos, 20)
            bullet.update(1000, dt)

        # Motion for each alien
        for i, alien in enumerate(aliens):
            if alien.pos.x + 100 >= float(screen.get_width()):
                alien_dir[i] = 0
            elif alien.pos.x <= 0:
                alien_dir[i] = 1
            alien.motion(300, dt, alien_dir[i])
            x_col = (bullet.pos.x >= alien.pos.x
                    and bullet.pos.x <= alien.pos.x + 100)
            y_col = (bullet.pos.y >= alien.pos.y
                     and bullet.pos.y <= alien.pos.y + 30)

            if x_col and y_col:
                shoot = False
                bullet.pos.x = player.pos.x + 50
                bullet.pos.y = player.pos.y - 15
                alien.health -= 10
                score += 10
                

        score_surface = font.render(f"Score {score}", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        screen.blit(score_surface, score_rect)
        
        pg.display.flip()
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == "__main__":
    main()
