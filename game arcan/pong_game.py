import arcade
import logging
import os

logging.basicConfig(level=logging.WARNING)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong Game"

BACKGROUND_COLOR = (235, 230, 220)  # Светлый бежевый
TEXT_COLOR = (60, 42, 34)  # Темно-коричневый
GAME_OVER_COLOR = (255, 69, 0)  # Оранжевый для Game Over


class Ball(arcade.Sprite):
    def __init__(self):
        if not os.path.exists('C:/Users/ksush/PycharmProjects/itproger/pg/game arcan/ball.png'):
            logging.warning("ball.png не найден")
        super().__init__('C:/Users/ksush/PycharmProjects/itproger/pg/game arcan/ball.png', 0.1)
        self.change_x = 3
        self.change_y = 3

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Отскок от границ экрана
        if self.right >= SCREEN_WIDTH or self.left <= 0:
            self.change_x *= -1
        if self.top >= SCREEN_HEIGHT or self.bottom <= 0:
            self.change_y *= -1


class Bar(arcade.Sprite):
    def __init__(self):
        if not os.path.exists('C:/Users/ksush/PycharmProjects/itproger/pg/game arcan/bar_2.png'):
            logging.warning("bar_2.png не найден")
        super().__init__('C:/Users/ksush/PycharmProjects/itproger/pg/game arcan/bar_2.png', 1.5)
        self.change_x = 0  # Инициализация изменения позиции

    def update(self):
        self.center_x += self.change_x
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left <= 0:
            self.left = 0


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bar = Bar()
        self.ball = Ball()
        self.setup()
        self.score = 0  # инициализация счетчика
        self.game_over = False  # завершение игры

    def setup(self):
        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT / 9
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        self.clear(BACKGROUND_COLOR)
        self.bar.draw()
        self.ball.draw()

        # отображение счета
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, TEXT_COLOR, 20)

        if self.game_over:
            arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             GAME_OVER_COLOR, 54, anchor_x="center", font_name="Arial")
            arcade.draw_text("Press R to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                             TEXT_COLOR, 20, anchor_x="center", font_name="Arial")

    def update(self, delta):
        if not self.game_over:
            # Проверка на столкновение между барьером и мячом
            if arcade.check_for_collision(self.bar, self.ball):
                self.ball.change_y = -abs(self.ball.change_y)
                self.ball.bottom = self.bar.top
                self.ball.change_y *= -1
                self.score += 1
                # Увеличение скорости мяча (по желанию)
                self.ball.change_x *= 1.1
            if self.ball.bottom <= 0:  # Проверка на конец игры
                self.game_over = True

            self.ball.update()
            self.bar.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.bar.change_x = 5
        if key == arcade.key.LEFT:
            self.bar.change_x = -5
        elif key == arcade.key.R and self.game_over:  # Перезапуск игры
            self.score = 0
            self.game_over = False
            self.setup()  # Сброс настроек игры

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.bar.change_x = 0


try:
    if __name__ == "__main__":
        window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.run()
except Exception as e:
    print(f"Произошла ошибка во время выполнения игры: {e}")
