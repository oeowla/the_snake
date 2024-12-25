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
        """Заготовка для отрисовки обьектов"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        """Инициализация атрибутов"""
        super().__init__()
        self.body_color = APPLE_COLOR
        """Позиция яблока на поле"""
        self.position = (
            ((randint(0, SCREEN_WIDTH)) // GRID_SIZE * GRID_SIZE),
            ((randint(0, SCREEN_HEIGHT)) // GRID_SIZE * GRID_SIZE)
        )

    def draw(self):
        """Отрисовка яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Генерация случайной позиции для яблока"""
        self.position = (
            ((randint(0, SCREEN_WIDTH)) // GRID_SIZE * GRID_SIZE),
            ((randint(0, SCREEN_HEIGHT)) // GRID_SIZE * GRID_SIZE)
        )


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

    def update_direction(self):
        """Метод для обновления направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки"""
        """движения змейки"""
        head = self.get_head_position()
        new_head = (head[0] + (self.direction[0] * GRID_SIZE),
                    head[1] + (self.direction[1] * GRID_SIZE))
        self.positions.insert(0, new_head)
        """Удаление последнего эллемента змейки"""
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        """Обработка краев экрана"""
        if self.positions[0][0] <= -20:
            self.positions[0] = (SCREEN_WIDTH - 20, self.positions[0][1])
        elif self.positions[0][0] >= SCREEN_WIDTH:
            self.positions[0] = (0, self.positions[0][1])
        elif self.positions[0][1] <= -20:
            self.positions[0] = (self.positions[0][0], SCREEN_HEIGHT - 20)
        elif self.positions[0][1] >= SCREEN_HEIGHT:
            self.positions[0] = (self.positions[0][0], 0)

    def draw(self):
        """Метод для отрисовки змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        """Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        """Затирания хвоста"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
    apple = Apple()
    snake = Snake()
    while True:
        """Основной цикл игры"""
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.update_direction()
        snake.move()
        snake.draw()
        snake_head = snake.get_head_position()
        if apple.position == snake_head:
            """Рост змеи"""
            snake.length += 1
            apple.randomize_position()
        if snake_head in snake.positions[1:]:
            """Проверка на столкновение змейки"""
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    """Запуск игры"""
    main()
