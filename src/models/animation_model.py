"""Модуль математической и физической модели игры Пинг-понг.

Содержит расчет координат объектов, симуляцию упругих столкновений
и логику ведения счета матча.
"""


class GameModel:
    """
    Описывает состояние мяча, ракеток игроков, правила их перемещения,
    а также алгоритмы обнаружения коллизий (столкновений).
    """

    def __init__(self, field_width: int, field_height: int) -> None:
        """Инициализирует начальное состояние игровых объектов.

        Args:
            field_width: Ширина игрового поля в пикселях.
            field_height: Высота игрового поля в пикселях.
        """
        self.width = field_width
        self.height = field_height

        #Параметры мяча
        self.ball_radius = 12
        self.ball_x = 0.0
        self.ball_y = 0.0
        self.ball_speed_x = 0.0
        self.ball_speed_y = 0.0
        self.initial_speed = 5.0  # Начальная скорость мяча
        self.speed_multiplier = 1.05  # Коэффициент ускорения при ударе

        #Параметры ракеток
        self.paddle_width = 15
        self.paddle_height = 90
        self.paddle_speed = 6.0  # Скорость перемещения ракеток

        # Позиции ракеток по оси X (с отступами от краев)
        self.left_paddle_x = 30
        self.right_paddle_x = self.width - 30 - self.paddle_width

        # Координаты Y (центрирование по вертикали)
        self.left_paddle_y = (self.height - self.paddle_height) / 2
        self.right_paddle_y = (self.height - self.paddle_height) / 2

        # Счёт игроков
        self.score_left = 0
        self.score_right = 0

        # Сброс мяча в центр поля для старта первой игры
        self.reset_ball(to_right=True)

    def reset_ball(self, to_right: bool) -> None:
        """Возвращает мяч в центр поля и задает начальное направление движения.

        Args:
            to_right: Если True, мяч летит вправо, иначе — влево.
        """
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        
        # Направление движения по X
        self.ball_speed_x = self.initial_speed if to_right else -self.initial_speed
        # Небольшое случайное или фиксированное смещение по Y для угла
        self.ball_speed_y = 3.0

    def move_left_paddle(self, direction: str) -> None:
        """Перемещает левую ракетку вверх или вниз с ограничением границ.

        Args:
            direction: Направление движения ('up' или 'down').
        """
        if direction == "up":
            self.left_paddle_y -= self.paddle_speed
            if self.left_paddle_y < 0:
                self.left_paddle_y = 0
        elif direction == "down":
            self.left_paddle_y += self.paddle_speed
            if self.left_paddle_y > self.height - self.paddle_height:
                self.left_paddle_y = self.height - self.paddle_height

    def move_right_paddle(self, direction: str) -> None:
        """Перемещает правую ракетку вверх или вниз с ограничением границ.

        Args:
            direction: Направление движения ('up' или 'down').
        """
        if direction == "up":
            self.right_paddle_y -= self.paddle_speed
            if self.right_paddle_y < 0:
                self.right_paddle_y = 0
        elif direction == "down":
            self.right_paddle_y += self.paddle_speed
            if self.right_paddle_y > self.height - self.paddle_height:
                self.right_paddle_y = self.height - self.paddle_height

    def reset_game(self) -> None:
        """Полностью сбрасывает счет матча и возвращает объекты в исходное состояние."""
        self.score_left = 0
        self.score_right = 0
        self.left_paddle_y = (self.height - self.paddle_height) / 2
        self.right_paddle_y = (self.height - self.paddle_height) / 2
        self.reset_ball(to_right=True)

    def update(self) -> None:
        """Обновляет физическое состояние: рассчитывает перемещения и коллизии."""
        # Движение мяча на основе текущей скорости
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        #Коллизии с верхней и нижней стенами поля
        if self.ball_y - self.ball_radius <= 0:
            self.ball_y = self.ball_radius
            self.ball_speed_y = -self.ball_speed_y  # Инверсия вектора движения
        elif self.ball_y + self.ball_radius >= self.height:
            self.ball_y = self.height - self.ball_radius
            self.ball_speed_y = -self.ball_speed_y

        #Коллизия с ЛЕВОЙ ракеткой
        # Проверяем, пересекает ли мяч левую границу ракетки по X
        if self.ball_speed_x < 0:  # Мяч должен лететь влево навстречу ракетке
            if (self.left_paddle_x <= self.ball_x - self.ball_radius <= self.left_paddle_x + self.paddle_width and
                    self.left_paddle_y <= self.ball_y <= self.left_paddle_y + self.paddle_height):
                # Происходит упругий отскок с ускорением мяча
                self.ball_speed_x = -self.ball_speed_x * self.speed_multiplier
                # Корректируем координату, чтобы избежать застревания в текстуре
                self.ball_x = self.left_paddle_x + self.paddle_width + self.ball_radius

        # Коллизия с ПРАВОЙ ракеткой
        # Проверяем, пересекает ли мяч правую границу ракетки по X
        if self.ball_speed_x > 0:  # Мяч должен лететь вправо навстречу ракетке
            if (self.right_paddle_x <= self.ball_x + self.ball_radius <= self.right_paddle_x + self.paddle_width and
                    self.right_paddle_y <= self.ball_y <= self.right_paddle_y + self.paddle_height):
                # Упругий отскок с ускорением мяча
                self.ball_speed_x = -self.ball_speed_x * self.speed_multiplier
                self.ball_x = self.right_paddle_x - self.ball_radius

        #Проверка гола (выход мяча за левую или правую стену)
        if self.ball_x < 0:
            # Гол в левые ворота — очко правому игроку
            self.score_right += 1
            self.reset_ball(to_right=True)  # Подача в сторону победителя
        elif self.ball_x > self.width:
            # Гол в правые ворота — очко левому игроку
            self.score_left += 1
            self.reset_ball(to_right=False)

