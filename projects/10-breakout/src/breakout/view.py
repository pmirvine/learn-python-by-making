"""Drawing the game. This is the only module that knows what anything looks like."""

import pygame

from breakout.model import Game, State


class View:
    """Draws a Game onto a small canvas, and scales it up to fill the window."""

    def __init__(self, game: Game, window: pygame.Surface) -> None:
        self.game = game
        self.window = window
        settings = game.settings
        self.canvas = pygame.Surface((settings.width, settings.height))
        self.font = pygame.font.Font(None, 16)

    def text(self, message: str, y: int, colour: str = "white") -> None:
        image = self.font.render(message, False, colour)
        x = (self.canvas.get_width() - image.get_width()) // 2
        self.canvas.blit(image, (x, y))

    def draw(self) -> None:
        game = self.game
        self.canvas.fill("black")

        for brick in game.level.bricks:
            pygame.draw.rect(self.canvas, brick.colour, brick.rect.inflate(-1, -1))
        pygame.draw.rect(self.canvas, "white", game.bat.rect)
        pygame.draw.rect(self.canvas, "yellow", game.ball.rect)

        status = f"SCORE {game.score:05}  LIVES {game.lives}  LEVEL {game.number + 1}"
        self.text(status, 4, "cyan")
        match game.state:
            case State.SERVE:
                self.text("PRESS SPACE TO SERVE", 150)
            case State.GAME_OVER:
                self.text("GAME OVER", 130, "red")
                self.text("PRESS SPACE", 150)
            case State.WON:
                self.text("YOU'VE CLEARED THE LOT!", 130, "yellow")
                self.text("PRESS SPACE", 150)

        scaled = pygame.transform.scale(self.canvas, self.window.get_size())
        self.window.blit(scaled, (0, 0))
