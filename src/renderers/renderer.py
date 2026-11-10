"""Модуль графического отображения игры Пинг-понг.
Отвечает за визуализацию всех игровых объектов.
"""

import tkinter as tk
from src.models.animation_model import GameModel


class GameRenderer:
    """Класс, отвечающий за отрисовку графических элементов игры.

    """

    def __init__(self, canvas: tk.Canvas, model: GameModel) -> None:
        """Инициализирует графический отрисовщик.

        Args:
            canvas: Холст Tkinter, на котором происходит рисование.
            model: Экземпляр математической модели данных игры.
        """
        self.canvas = canvas
        self.model = model

    def render(self) -> None:
        """Очищает холст и заново отрисовывает все игровые объекты."""
        # Полная очистка холста перед каждым новым кадром анимации
        self.canvas.delete("all")

        #1. Отрисовка центральной разделительной линии
        self.canvas.create_line(
            self.model.width // 2, 0,
            self.model.width // 2, self.model.height,
            fill="#333333", width=2, dash=(10, 10)
        )

        #2. Отрисовка текущего счета игроков
        # Счет левого игрока
        self.canvas.create_text(
            self.model.width // 4, 50,
            text=str(self.model.score_left),
            fill="#ffffff", font=("Helvetica", 36, "bold")
        )
        # Счет правого игрока
        self.canvas.create_text(
            (self.model.width // 4) * 3, 50,
            text=str(self.model.score_right),
            fill="#ffffff", font=("Helvetica", 36, "bold")
        )

        #3. Отрисовка левой ракетки
        self.canvas.create_rectangle(
            self.model.left_paddle_x,
            self.model.left_paddle_y,
            self.model.left_paddle_x + self.model.paddle_width,
            self.model.left_paddle_y + self.model.paddle_height,
            fill="#00ff88", outline=""
        )

        #4. Отрисовка правой ракетки
        self.canvas.create_rectangle(
            self.model.right_paddle_x,
            self.model.right_paddle_y,
            self.model.right_paddle_x + self.model.paddle_width,
            self.model.right_paddle_y + self.model.paddle_height,
            fill="#00e1ff", outline=""
        )

        #5. Отрисовка игрового мяча
        self.canvas.create_oval(
            self.model.ball_x - self.model.ball_radius,
            self.model.ball_y - self.model.ball_radius,
            self.model.ball_x + self.model.ball_radius,
            self.model.ball_y + self.model.ball_radius,
            fill="#ff0055", outline=""
        )

