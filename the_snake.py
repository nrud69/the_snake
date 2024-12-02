from random import randint
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

CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=CENTER, body_color=None):
        """Инициализация базового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Функция рисования объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, которое появляется на игровом поле."""

    def __init__(self):
        """Инициализация яблока и случайная его позиция."""
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Рисует яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи, которая перемещается по экрану."""

    def __init__(self):
        """Инициализация змейки и ее начальных параметров."""
        super().__init__()
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление змейки, если оно изменилось."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Рисует змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку в текущем направлении."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Вычисляем новую позицию головы
        head_x, head_y = self.positions[0]
        move_x, move_y = self.direction
        new_head_position = (
            (head_x + move_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + move_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Добавляем новую позицию головы в начало списка
        self.positions.insert(0, new_head_position)

        # Удаляем хвост, если длина змейки осталась прежней
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает параметры змейки в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и изменяет направление движения змейки."""
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
    """Основная игровая функция."""
    # Инициализация PyGame:
    pygame.init()

    # Создаём экземпляры классов
    apple = Apple()
    snake = Snake()

    while True:
        # Управляем частотой обновления экрана:
        clock.tick(SPEED)

        # Обрабатываем ввод пользователя
        handle_keys(snake)

        # Двигаем змейку
        snake.move()

        # Проверяем столкновение змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            pygame.time.delay(500)  # Задержка перед сбросом
            snake.reset()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            apple.randomize_position()  # Перемещаем яблоко

        # Отрисовываем игровой экран
        screen.fill(BOARD_BACKGROUND_COLOR)  # Чёрный фон
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки
        pygame.display.flip()  # Обновление экрана

    pygame.quit()


if __name__ == '__main__':
    main()
