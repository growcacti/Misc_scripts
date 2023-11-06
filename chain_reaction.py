import pygame as pg
import random


class Cell(pg.sprite.Sprite):
    def __init__(self, x, y, size, color, velocity):
        super().__init__()
        # Use SRCALPHA for transparency
        self.image = pg.Surface(size, pg.SRCALPHA)

        # Draw ellipse on the surface
        pg.draw.ellipse(self.image, color, self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.velocity = velocity

    def inflate(self, amount):
        new_width = int(self.size[0] + amount)
        new_height = int(self.size[1] + amount)
        self.size = (new_width, new_height)
        color = (
            random.randint(
                20, 100), random.randint(
                20, 100), random.randint(
                20, 185))

        # Create a new transparent surface and draw the new ellipse onto it
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        pg.draw.ellipse(self.image, color, self.image.get_rect())

        # Adjust the rect object to fit the new size and keep the center
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # You might want to add boundary checking here to reverse velocity or
        # remove cell when it reaches the screen boundary.


class Game:
    def __init__(self):
        # Initialize pg
        pg.init()

        # Game variables
        self.level = 1
        # Increase speed by 0.5 for each level
        self.cell_speed = 1 + (self.level - 1) * 0.5
        self.points = 0
        self.lives = 3

        # Display settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height))
        pg.display.set_caption("Cell Reaction")

        # cell settings
        self.min_cell_size = 2
        self.max_cell_size = 20

        # Absorber settings
        self.absorber_size = (
            self.screen_width // 10,
            self.screen_height // 10)

        self.absorber_color = (
            random.randint(
                20, 100), random.randint(
                20, 100), random.randint(
                20, 185))

        self.all_sprites = pg.sprite.Group()

    def level_up(self):
        self.level += 1
        # Increase speed by 0.5 for each level
        self.cell_speed = 1 + (self.level - 1) * 0.5
        all_sprites.add(absorber)
        for _ in range(10):
            cell = self.create_random_cell()
            self.all_sprites.add(cell)

    def create_random_cell(self):
        x = random.randint(0, self.screen_width - self.max_cell_size)
        y = random.randint(0, self.screen_height - self.max_cell_size)
        size = random.randint(self.min_cell_size, self.max_cell_size)
        velocity = [random.choice([-1, 1]) * self.cell_speed,
                    random.choice([-1, 1]) * self.cell_speed]
        color = (
            random.randint(
                50, 175), random.randint(
                50, 175), random.randint(
                50, 170))
        # changed cell -> Cell
        return Cell(x, y, (size, size), color, velocity)

    def game_over(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        font = pg.font.Font(None, 48)  # Adjust font size as needed
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(
            game_over_text,
            (self.screen_width //
             2 -
             game_over_text.get_width() //
             2,
             self.screen_height //
             2 -
             game_over_text.get_height() //
             2))
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False

    def main(self):
        all_sprites = pg.sprite.Group()  # Group to store all sprites
        absorber = None  # cell created by a mouse click
        points = 0
        # Populate the screen with random cells
        num_cells = 150  # Adjust the number of cells as desired
        lives = 3

        for i in range(num_cells):
            cell = self.create_random_cell()
            all_sprites.add(cell)

        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        if absorber is None and lives > 0:  # Check if there's no current absorber and if lives remain
                            absorber = Cell(mouse_x -
                                            self.absorber_size[0] //
                                            2, mouse_y -
                                            self.absorber_size[1] //
                                            2, self.absorber_size, self.absorber_color, [0, 0])
                            all_sprites.add(absorber)
                            lives -= 1  # Decrement the lives counter
            has_collided = False  # Initialize the flag before checking collisions
            if absorber is not None:  # Perform cell collision check only if absorber exists
                for cell in all_sprites.sprites():
                    if cell != absorber and pg.sprite.collide_rect(
                            absorber, cell):
                        if cell.size[0] <= absorber.size[0] and cell.size[1] <= absorber.size[1]:
                            absorber.inflate(3)
                            points += 1
                            cell.kill()
                        elif cell.size[0] >= absorber.size[0] and cell.size[1] >= absorber.size[1]:
                            absorber.inflate(5)
                            points -= 1

            if not has_collided and absorber is not None:  # Check for non-collision after the loop
                # Deflate the absorber by 1 unit
                absorber.inflate(-0.0000000000000001)
                if absorber.size[0] <= 1 or absorber.size[1] <= 1:
                    all_sprites.remove(absorber)
                    all_sprites.add(absorber)
                    # lives -= 1  # Decrement the lives counter# Remove
                    # absorber from all_sprites group

                    cell.kill()

            all_sprites.update()
            if lives == 0 and (
                    absorber is None or absorber.size[0] <= 1 or absorber.size[1] <= 1):
                self.game_over()  # Display game over screen
                running = False  # End the main game loop
            self.screen.fill((255, 244, 255, 255))  # Clear the screen

            all_sprites.draw(self.screen)  # Draw all sprites onto the screen

            # Display the point value
            font = pg.font.Font(None, 36)
            points_text = font.render(f"Points: {points}", True, (15, 10, 15))
            # lives_text = font.render(f"Lives: {lives}", True, (5, 55, 10))
            # self.screen.blit(lives_text, (10, 40))  # Adjust position as
            # necessary

            self.screen.blit(points_text, (10, 10))

            pg.display.flip()
            clock.tick(30)  # Adjust the desired frame rate (e.g., 60 FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
