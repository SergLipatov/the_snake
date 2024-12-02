"""
Модуль игры Змейка.

Содержащит описание классов,
функций и игровой механики игры змейка.
"""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Центр поля
BOARD_CЕNTЕR = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Словарь для обработки нажатий клавиш
# (нажатая клавиша, старое направление): новое направление
KEYBOARD_MAPS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT}


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self) -> None:
        """Метод инициализации экземпляров класса GameObject."""
        self.position = BOARD_CЕNTЕR
        self.body_color = None

    def draw():
        """Метод отрисовки игровых объектов."""
        raise NotImplementedError('Метод переопределяется в наследниках.')


class Snake(GameObject):
    """Класс описывающий змейку в игре."""

    def __init__(self):
        """Метод инициализации экземпляров класса Snake."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.reset()

    def draw(self):
        """Метод реализующий движение змейки."""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Функция возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод реализующий движение змейки."""
        head_position_x, head_position_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head_position_x = head_position_x + GRID_SIZE * delta_x
        new_head_position_y = head_position_y + GRID_SIZE * delta_y
        real_head_position_x = new_head_position_x % SCREEN_WIDTH
        real_head_position_y = new_head_position_y % SCREEN_HEIGHT
        self.last = self.positions[-1]
        self.positions.insert(0, (real_head_position_x, real_head_position_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние."""
        self.length = 1
        self.positions = [BOARD_CЕNTЕR]
        self.last = None
        self.direction = choice((UP, DOWN, RIGHT, LEFT))


class Apple(GameObject):
    """Класс описывающий поведение яблока."""

    def __init__(self, occupied_cells=None):
        """
        Метод инициализации экземпляров класса Apple.

        Args:
            occupied_cells (list): Список уже занятых ячеек поля
        Returns:
            None
        """
        super().__init__()
        if occupied_cells is None:
            occupied_cells = (BOARD_CЕNTЕR)
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """
        Метод устанавливающий случайную позицию яблока из свободных.

        Args:
            occupied_cells (list): Список уже занятых ячеек поля
        Returns:
            None
        """
        if not hasattr(occupied_cells, '__iter__') or occupied_cells is None:
            occupied_cells = (BOARD_CЕNTЕR)
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Метод отрисовывающий яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Метод отслеживающий нажатие клавиш управления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Вы вышли из игры.')
        if event.type == pg.KEYDOWN:
            game_object.next_direction = KEYBOARD_MAPS.get(
                (event.key, game_object.direction))


def main():
    """Главная функция игровой механики."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head_cells = snake.get_head_position()
        if snake.positions.count(head_cells) > 1:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        elif head_cells == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
