
import arcade
import random
import time
import pathlib

from game.key_handler import KeyHandler
from game.on_draw import Draws
from game.power_ups import PowerUps
from game.update import Update
from game.players import Players
from game.box_draw import BoxDrawer
from game.score import Score
from game.winner_window.winner_message import WinnerView


class PongGame(arcade.View):
    """Pong game is a game with to players
    where they try to get the ball reaches
    the enemy side so that they can make points.
    Sterio Type:
        Visual Game.
    Attributes:
        self.players: a SpriteList() for the two players.
        self.ball: a SpriteList() for the game ball.
        self.wall_list: a SpriteList() for the walls.
        self.limits_list: a SpriteList() for the limits of the game screen for objects.
        self.all_sprites: a SpriteList() for all the sprites (players and ball).
        self._players: the Players() class.
        self.output: a string.
        self.collided: a boolean value.
        self.score_p1: a interger value.
        self.score_p1: a interger value."""

    def __init__(self, width: int, height: int, title: str):
        """The constructor class, which
        makes the screen game to appear."""

        super().__init__()

        # Set up the empty Sprites.
        self.players = arcade.SpriteList()
        self.ball = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.limit_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.power_ups = arcade.SpriteList()

        self._players = Players()
        self._power_up = PowerUps()

        self.height = height
        self.width = width
        self.title = title

        self.power = "no power"
        self.output = ""
        self.collided = False
        self.paused = False
        self.score_p1 = 0
        self.score_p2 = 0

    def setup(self):
        """Sets the background color, the players,
        and ball.
        In the future it will be used for power ups and
        sounds/musics."""

        # Setup the backgound color
        arcade.set_background_color(arcade.color.GRAY)

        self.player1 = self._players.player_maker(
            self.height, "img/player1_plataform.png", 20)
        self.player2 = self._players.player_maker(
            self.height, "img/player2_plataform.png", 730)

        self.power_up1 = self._power_up.draw_power("img/power_up1.png")
        self.power_up2 = self._power_up.draw_power("img/power_up2.png")
        self.power_up3 = self._power_up.draw_power("img/power_up3.png")
        self.power_up4 = self._power_up.draw_power("img/power_up4.png")

        self.all_sprites.append(self.player1)
        self.all_sprites.append(self.player2)
        self.power_ups.append(self.power_up1)
        self.power_ups.append(self.power_up2)
        self.power_ups.append(self.power_up3)
        self.power_ups.append(self.power_up4)

        # Create horizontal rows of boxes
        for x in range(0, self.width):
            # Bottom edge
            self.wall_list.append(BoxDrawer.box_drawer(
                x, self.height, self.width, "xbottom"))

            # Top edge
            self.wall_list.append(BoxDrawer.box_drawer(
                x, self.height, self.width, "xtop"))

        for y in range(0, self.height):
            # Bottom edge
            self.limit_list.append(BoxDrawer.box_drawer(
                y, self.height, self.width, "ybottom"))

            # Top edge
            self.limit_list.append(BoxDrawer.box_drawer(
                y, self.height, self.width, "ytop"))

        # Create ball
        ball = arcade.Sprite(pathlib.Path(
            __file__).parent / "img/ball.png", 0.25)
        ball.center_x = random.randrange(499, 500)
        ball.center_y = random.randrange(299, 300)
        while ball.change_x == 0 and ball.change_y == 0:
            directions = [-4, -3, -2, -1, 1, 2, 3, 4, 5]
            ball.change_x = random.randrange(-4, 5)
            ball.change_y = random.choice(directions)

        self.all_sprites.append(ball)

        for i in self.wall_list:
            self.all_sprites.append(i)
        self.players.append(self.player1)
        self.players.append(self.player2)
        self.ball.append(ball)

        self.all_sprites.append(self.power_up1)
        self.all_sprites.append(self.power_up2)
        self.all_sprites.append(self.power_up3)
        self.all_sprites.append(self.power_up4)

    def on_key_press(self, symbol, modifiers):

        KeyHandler(self.player1).on_key_press_a(
            symbol, modifiers, self.power)
        KeyHandler(self.player2).on_key_press_b(
            symbol, modifiers, self.power)

        if symbol == arcade.key.P:
            self.paused = not self.paused

    def on_key_release(self, symbol: int, modifiers: int):

        KeyHandler(self.player1).on_key_release_a(
            symbol, modifiers)
        KeyHandler(self.player2).on_key_release_b(
            symbol, modifiers)

    def on_update(self, delta_time: float):
        """for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )"""

        # If paused, don't update anything
        if self.paused:
            directions = [-4, -3, -2, -1, 1, 2, 3, 4, 5]
            self.players[0].center_y = 300
            self.players[1].center_y = 300
            self.all_sprites[2].center_y = 300
            self.all_sprites[2].change_x = random.choice(directions)
            time.sleep(2)
            self.paused = False

        # Update everything
        self.all_sprites.update()

        # This part is responsible for detecting when a player gets a point
        limits_hit = arcade.check_for_collision_with_list(
            self.all_sprites[2], self.limit_list)

        for limit in limits_hit:

            x_position = self.all_sprites[2]._get_center_x()

            if self.all_sprites[2].change_x > 0:
                self.all_sprites[2].center_x = random.randrange(499, 500)
                self.all_sprites[2].center_y = random.randrange(300, 400)
                self.all_sprites[2].top = limit.bottom

            elif self.all_sprites[2].change_x < 0:
                self.all_sprites[2].center_x = random.randrange(499, 500)
                self.all_sprites[2].center_y = random.randrange(300, 400)
                self.all_sprites[2].bottom = limit.top

            if x_position >= 740:
                if self.power == "no power":
                    self.score_p1 += 1
                elif self.power == "blue":
                    self.score_p2 += 1
                else:
                    self.score_p1 += 1
                power_chance = random.randrange(1, 4)
                self.power_ups[power_chance].center_x = random.randrange(
                    200, 600)
                self.power_ups[power_chance].center_y = random.randrange(
                    200, 400)
                self.power = "no power"
                self.all_sprites[1].center_x = 750
                self.all_sprites[0].center_x = 50
                self.paused = True

            elif x_position <= 54:
                if self.power == "no power":
                    self.score_p2 += 1
                elif self.power == "blue":
                    self.score_p1 += 1
                else:
                    self.score_p2 += 1
                power_chance = random.randrange(0, 3)
                self.power_ups[power_chance].center_x = random.randrange(
                    200, 600)
                self.power_ups[power_chance].center_y = random.randrange(
                    200, 400)
                self.power = "no power"
                self.all_sprites[1].center_x = 750
                self.all_sprites[0].center_x = 50
                self.paused = True

        x_position = self.all_sprites[2]._get_center_x()

        if x_position <= 35:
            self.all_sprites[2].center_x = random.randrange(499, 500)
            self.all_sprites[2].center_y = random.randrange(300, 400)

        # We can use the following code to give a second chance for the players!

        if self.score_p2 == 5:
            print("Player 2 Wins the game")
            winner_view = WinnerView("2")
            # Create a new Pong Game window
            winner_view.setup()

            self.window.show_view(winner_view)

        if self.score_p1 == 5:

            print("Player 1 Wins the game")
            winner_view = WinnerView("1")
            # Create a new Pong Game window
            winner_view.setup()

            self.window.show_view(winner_view)

        # Keep the player on screen
        returned_value = Update(self.all_sprites, self.wall_list, self.players, self.limit_list, self.power_ups,
                                self.height).update(delta_time)

        if returned_value == "green":
            self.power = "green"

        elif returned_value == "red":
            self.all_sprites[0].center_x = 100
            self.all_sprites[1].center_x = 680

        elif returned_value == "blue":
            self.all_sprites[0].center_x = 750
            self.all_sprites[1].center_x = 50
            self.power = "blue"

        elif returned_value == "yellow":
            self.power = "yellow"

        self.draw()

    def draw(self):
        """Draws all the information unto the screen."""
        Draws(self.all_sprites, self.output).on_draw()
        Score.draw_score(self)