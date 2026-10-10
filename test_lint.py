"""Тестовый файл для проверки линтера Ruff, Pyright и ErrorLens в VSCodium.

Попробуйте:
1. Раскомментировать строку с ошибкой типов ниже и увидеть мгновенную подсветку ErrorLens.
2. Испортить отступы или кавычки и нажать Ctrl+S (Ruff автоматически отформатирует код).
"""

from dataclasses import dataclass
from typing import Final

MAX_SCORE: Final[int] = 100


@dataclass
class Stats:
    user: str
    points: int
    is_active: bool

    def calculate_percent(self) -> float:
        """Вычисляет процент выполнения от максимума."""
        return (self.points / MAX_SCORE) * 100.0


def greet(stats: Stats) -> str:
    """Генерирует приветствие со статистикой."""
    percent = stats.calculate_percent()
    return f"Привет, {stats.user}! Прогресс: {percent:.1f}% (Статус: {'Активен' if stats.is_active else 'Неактивен'})"


# Тестовый запуск
demo_stats = Stats(user="dimonjolo", points=95, is_active=True)
message = greet(demo_stats)
print(message)

# ТЕСТ ERROR LENS: Если раскомментировать строку ниже, Pyright и ErrorLens сразу покажут ошибку типов прямо в строке!
# bad_calc = greet(12345)  # <-- Argument of type "int" cannot be assigned to parameter "stats" of type "Stats"
