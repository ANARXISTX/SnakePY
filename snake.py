import pygame as pg
import random
from enum import Enum

# Инициализация pygame
pg.init()

# Константы
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Направления движения
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# Настройка окна
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Snake Game")
clock = pg.time.Clock()


class Snake:

    def __init__(self):
        self.positions = [(WINDOW_SIZE // 2, WINDOW_SIZE // 2)]
        self.direction = Direction.RIGHT
        self.length = 1
        

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == Direction.UP:
            y -= GRID_SIZE
        elif self.direction == Direction.DOWN:
            y += GRID_SIZE
        elif self.direction == Direction.LEFT:
            x -= GRID_SIZE
        elif self.direction == Direction.RIGHT:
            x += GRID_SIZE

        # Проверка границ
        if x >= WINDOW_SIZE:
            x = 0
        elif x < 0:
            x = WINDOW_SIZE - GRID_SIZE
        if y >= WINDOW_SIZE:
            y = 0
        elif y < 0:
            y = WINDOW_SIZE - GRID_SIZE

        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for pos in self.positions:
            pg.draw.rect(surface, GREEN,
                         (pos[0], pos[1], GRID_SIZE - 2, GRID_SIZE - 2))


class Apple:

    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        return (random.randint(0, GRID_COUNT - 1) * GRID_SIZE,
                random.randint(0, GRID_COUNT - 1) * GRID_SIZE)

    def draw(self, surface):
        pg.draw.rect(
            surface, RED,
            (self.position[0], self.position[1], GRID_SIZE - 2, GRID_SIZE - 2))


def main():
    snake = Snake()
    apple = Apple()
    score = 0
    font = pg.font.Font(None, 36)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and snake.direction != Direction.DOWN:
                    snake.direction = Direction.UP
                elif event.key == pg.K_DOWN and snake.direction != Direction.UP:
                    snake.direction = Direction.DOWN
                elif event.key == pg.K_LEFT and snake.direction != Direction.RIGHT:
                    snake.direction = Direction.LEFT
                elif event.key == pg.K_RIGHT and snake.direction != Direction.LEFT:
                    snake.direction = Direction.RIGHT

        # Обновление змейки
        snake.update()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            apple.position = apple.randomize_position()

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            pg.quit()
            return

        # Проверка победы
        if score >= 10:
            screen.fill(BLACK)
            win_text = font.render("Победа!", True, WHITE)
            screen.blit(win_text,
                        (WINDOW_SIZE // 2 - win_text.get_width() // 2,
                         WINDOW_SIZE // 2 - win_text.get_height() // 2))
            pg.display.flip()
            pg.time.wait(2000)
            pg.quit()
            return

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)

        # Отображение счета
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pg.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
