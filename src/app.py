"""Модуль главного управляющего класса приложения.
Содержит настройку окна Tkinter, обработку клавиатурного ввода
и игровой цикл анимации.
"""

import tkinter as tk
from src.models.animation_model import GameModel
from src.renderers.renderer import GameRenderer


class App:
    """Главный класс приложения игры Пинг-понг.

    Управляет инициализацией графического окна, холста для рисования,
    отслеживанием нажатий клавиш и периодическим обновлением игрового экрана.
    """

    def __init__(self) -> None:
        """Инициализирует графическое окно приложения и его параметры."""
        self.root = tk.Tk()
        self.root.title("Пинг-понг — Практикум по программированию")
        self.root.resizable(False, False)

        # Константы размеров окна игры
        self.width = 800
        self.height = 600

        # Создание Canvas для отрисовки графики
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack()

        # Инициализация модели данных и графического отрисовщика
        self.model = GameModel(self.width, self.height)
        self.renderer = GameRenderer(self.canvas, self.model)

        # Флаг состояния игры (активна/пауза)
        self.is_running = True

        # Словарь для отслеживания одновременно зажатых клавиш
        self.pressed_keys = {
            "w": False,
            "s": False,
            "Up": False,
            "Down": False
        }

        # Привязка обработчиков событий нажатия и отпускания клавиш
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)

        # Частота обновления кадров (в миллисекундах) — примерно 60 FPS
        self.fps_delay = 16

    def _on_key_press(self, event: tk.Event) -> None:
        """Обрабатывает нажатия клавиш на клавиатуре.
        Args:
            event: Объект события Tkinter, содержащий информацию о клавише.
        """
        key = event.keysym
        
        # Обработка паузы и сброса
        if key == "space":
            self.is_running = not self.is_running
        elif key in ("r", "R", "К", "к"):
            self.model.reset_game()
        
        # Фиксация зажатых клавиш перемещения ракеток
        if key in ("w", "W", "ц", "Ц"):
            self.pressed_keys["w"] = True
        elif key in ("s", "S", "ы", "Ы"):
            self.pressed_keys["s"] = True
        elif key == "Up":
            self.pressed_keys["Up"] = True
        elif key == "Down":
            self.pressed_keys["Down"] = True

    def _on_key_release(self, event: tk.Event) -> None:
        """Обрабатывает событие отпускания клавиш клавиатуры.

        Args:
            event: Объект события Tkinter.
        """
        key = event.keysym
        
        # Сброс флага при отпускании клавиши
        if key in ("w", "W", "ц", "Ц"):
            self.pressed_keys["w"] = False
        elif key in ("s", "S", "ы", "Ы"):
            self.pressed_keys["s"] = False
        elif key == "Up":
            self.pressed_keys["Up"] = False
        elif key == "Down":
            self.pressed_keys["Down"] = False

    def _process_input(self) -> None:
        """Проверяет состояние зажатых клавиш и двигает ракетки."""
        # Левая ракетка (W / S)
        if self.pressed_keys["w"]:
            self.model.move_left_paddle("up")
        if self.pressed_keys["s"]:
            self.model.move_left_paddle("down")
            
        # Правая ракетка (Стрелки Вверх / Вниз)
        if self.pressed_keys["Up"]:
            self.model.move_right_paddle("up")
        if self.pressed_keys["Down"]:
            self.model.move_right_paddle("down")

    def _game_loop(self) -> None:
        """Основной игровой цикл, обновляющий состояние и графику."""
        if self.is_running:
            # Опрос зажатых клавиш клавиатуры
            self._process_input()
            # Расчет физики движения и столкновений мяча
            self.model.update()
            
        # Отрисовка обновленного кадра (работает даже на паузе для визуализации счета)
        self.renderer.render()

        # Рекурсивный вызов следующего кадра через заданный интервал времени
        self.root.after(self.fps_delay, self._game_loop)

    def run(self) -> None:
        """Запускает игровой цикл анимации и главное окно приложения."""
        self._game_loop()
        self.root.mainloop()

