from random import randint

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


# Тут опишите все классы игры.
class GameObject:
    """Основной класс для всех игровых объектов."""

    def __init__(self, body_color=None, position=None):
        self.position = self.position = position if position is not None else (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объектов"""
        raise NotImplementedError(
            f'Класс {self.__class__.__name__} должен реализовать метод draw()'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко в игре."""

    def __init__(self, body_color=APPLE_COLOR, position=None):
        super().__init__(body_color, position)
        if position is None:
            self.randomize_position()

    def randomize_position(self, occupied_positions=()):
        """Размещает яблоко  в случайной клетке"""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_positions:
                self.position = position
                return

    def draw(self):
        """Метод draw класса Apple."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Свойства Змейки"""

    def __init__(self, body_color=SNAKE_COLOR, position=None):
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет направление после нажатия клавиши"""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction  # Распаковываем кортеж направления
        new_head_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT

        new_head_position = (new_head_x, new_head_y)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
        return new_head_position

    def draw(self):
        """Метод draw класса Snake"""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки"""
        return self.positions[0]

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def reset(self):
        """Сбрасывает состояние змейки до начального"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация pg."""
    pg.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        new_head_position = snake.move()

        snake_head_pos = snake.get_head_position()
        apple_pos = apple.position

        if snake_head_pos == apple_pos:
            snake.grow()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
