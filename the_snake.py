from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс объектов игры"""

    def __init__(self) -> None:
        self.position = BOARD_CЕNTЕR
        self.body_color = None

    def draw(self):
        """Метод отрисовки игровых объектов"""


class Snake(GameObject):
    """Класс описывающий змейку в игре"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.lenght = 1
        self.next_direction = None
        self.positions = [BOARD_CЕNTЕR]
        self.last = None
        self.direction = choice([UP, DOWN, RIGHT, LEFT])

    def draw(self):
        """Метод реализующий движение змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Функция возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод реализующий движение змейки"""
        old_positions = self.get_head_position()
        dX = old_positions[0] // GRID_SIZE + self.direction[0]
        dY = old_positions[1] // GRID_SIZE + self.direction[1]
        if dX < 0 and self.direction == LEFT:
            dX = GRID_WIDTH - 1
        if dX > GRID_WIDTH - 1 and self.direction == RIGHT:
            dX = 0
        if dY < 0 and self.direction == UP:
            dY = GRID_HEIGHT - 1
        if dY > GRID_HEIGHT - 1 and self.direction == DOWN:
            dY = 0
        self.last = self.positions[len(self.positions) - 1]
        self.positions.insert(0, (dX * GRID_SIZE, dY * GRID_SIZE))
        if len(self.positions) > self.lenght:
            self.positions.pop(-1)

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние"""
        self.lenght = 1
        self.positions = [BOARD_CЕNTЕR]
        self.last = None
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывающий поведение яблока"""

    def randomize_position(self):
        """Метод устанавливающий случайную позицию яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """Метод отрисовывающий яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Метод отслеживающий нажатие клавиш управления"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игровой механики"""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
            apple.randomize_position()
        elif snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
