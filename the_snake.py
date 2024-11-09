import pygame
from random import randint

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

# Цвет фона - чёрный:
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс для объектов на поле игры."""

    def __init__(self, position, body_color):
        """
        Инициализация объекта с заданной позицией и цветом.

        :param position: Позиция объекта
        :param body_color: Цвет объекта
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс для яблок в игре."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        super().__init__((0, 0), APPLE_COLOR)  # Call parent constructor with dummy position
        self.randomize_position()

    def randomize_position(self):
        """Установка случайного положения яблока на поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки с одной клеткой."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR) 
        self.length = 1
        self.position = [self.position] 
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возврат позиции головы змейки."""
        return self.position[0]

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки на одну ячейку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                             (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Проверка на столкновение
        if new_head_position in self.position[1:]:
            self.reset()
            return

        self.position.insert(0, new_head_position)
        if len(self.position) > self.length:
            self.position.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.position:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обработка управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
