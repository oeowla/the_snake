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

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центр игрового окна:
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


class GameObject():
    """Родительский класс обьектов игры"""

    def __init__(self) -> None:
        """Инициализация атрибутов"""
        self.position = CENTER
        self.body_color = None

    def draw(self):
        """Метод отрисовки для переоределения в дочерних классах"""

    def draw_cell(self, position, body_color=None, field=BORDER_COLOR):
        """Метод отрисовки одной ячейки"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, field, rect, 1)


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, snake_poss=None):
        """Инициализация атрибутов"""
        super().__init__()
        self.body_color = APPLE_COLOR
        """Позиция яблока на поле"""
        self.position = self.randomize_position(snake_poss)

    def draw(self):
        """Отрисовка яблока на игровом поле"""
        self.draw_cell(self.position, self.body_color)

    def randomize_position(self, snake_poss=None):
        """Генерация случайной позиции для яблока"""
        if snake_poss is None:
            snake_poss = []
        while True:
            apple_poss = ((randint(0, (GRID_WIDTH - 1)) * GRID_SIZE),
                          (randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE))
            if apple_poss not in snake_poss:
                break
        return apple_poss


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        """Инициализация атрибутов"""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Метод для получения позиции головы змейки"""
        return self.positions[0]

    def update_direction(self, next_direction=None):
        """Метод для обновления направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки"""
        """движения змейки"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        self.positions.insert(0, ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                                  (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки"""
        self.draw_cell(self.positions[0], self.body_color)
        """Затирания хвоста"""
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR,
                           BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1
        list.clear(self.positions)
        list.append(self.positions, CENTER)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция для обработки нажатия клавиш"""
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
    """Инициализация pygame"""
    pygame.init()
    """Создание экземпляров класс"""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        """Основной цикл игры"""
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snale_head = snake.get_head_position()
        if apple.position == snale_head:
            """Рост змеи"""
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        if snale_head in snake.positions[3:]:
            """Проверка на столкновение змейки"""
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    """Запуск игры"""
    main()
