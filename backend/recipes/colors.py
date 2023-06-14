from django.db import models


class HexColors(models.TextChoices):
    RED = '#C11B0E', 'Красный'
    ORANGE = '#FFA500', 'Оранжевый'
    YELLOW = '#FFFF00', 'Желтый'
    GREEN = '#008000', 'Зеленый'
    BLUE = '#0000FF', 'Синий'
    PURPLE = '#800080', 'Фиолетовый'
    GRAY = '#808080', 'Серый'
    BLACK = '#030100', 'Черный'
