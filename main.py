import pygame as pg
import random 

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
        self.bullet = Bullet(self.pos)

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

# ------- Function to display message on screen where we please ----------
def display_message(message, font, screen, color, pos, zone):
            message_surface = font.render(message, True, color)
            message_rect = message_surface.get_rect()

            if zone == "tl":
                message_rect.topleft = pos
            elif zone == "c":
                message_rect.center = pos
            screen.blit(message_surface, message_rect)

# --------- MAIN FUNC -------------
def main():
    # Setup
    alien_count = int(input("How many aliens would you like to destroy?: "))

    # Variables needed for Pygame
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Nama Invaders!")
    running = True
    font = pg.font.Font(None, 36)
    dt = 0

    # Variables for player
    shoot = False  
    player = Player(screen, "white")
    score = 0

    # Variables for computing time elapsed
    clock = pg.time.Clock()
    start_time = pg.time.get_ticks()
    time_limit = alien_count

    # Variables and setup for aliens
    aliens = []
    alien_dir = [1] * alien_count
    dead = 0
    used = set()
    for i in range(alien_count):
        v_mul = random.randint(1, 5)
        while v_mul in used:
            v_mul = random.randint(1, 5)
        aliens.append(Alien(screen, v_mul))
        time_limit += v_mul * 5 
        used.add(v_mul)

    # Game's main loop
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")
        keys = pg.key.get_pressed()
        pg.draw.rect(screen, player.color, player.rect, 40)
        elapsed_seconds = (pg.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, time_limit - elapsed_seconds)

        # If all aliens dead -> win, time = 0 -> lose, else regular game logic
        if dead == alien_count:
            display_message("You Win!!", font, screen, (0, 255, 0), 
                            (screen.get_width() / 2, screen.get_height() / 2), "c")
            display_message(f"Score: {score}", font, screen, (0, 255, 0),
                            (screen.get_width() / 2, screen.get_height() / 2 + 40), "c")
        elif remaining_time == 0:
            display_message("You Lose :(", font, screen, (255, 0, 0), 
                            (screen.get_width() / 2, screen.get_height() / 2), "c")
            display_message(f"Score: {score}", font, screen, (255, 0, 0),
                            (screen.get_width() / 2, screen.get_height() / 2 + 40), "c")
        else:
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

                # Alien being hit update
                if alien.health and alien.collision(player.bullet.pos) and shoot:
                    shoot = False
                    alien.health -= 10
                    score += 10
                    if alien.health == 0:
                        dead += 1


            # Time left display
            display_message(f"Time left: {remaining_time}s", font, screen,
                            (255, 255, 255), (10, 40), "tl")

            # Score display
            display_message(f"Score: {score}", font, screen, 
                            (255, 255, 255), (10, 10), "tl")
        
        pg.display.flip()
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == "__main__":
    main()
