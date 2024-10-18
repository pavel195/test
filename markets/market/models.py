from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название рынка

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название единицы измерения

    def __str__(self):
        return self.name


class MarketUnitPriority(models.Model):
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE
    )  # Связь с моделью Market
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)  # Связь с моделью Unit
    priority = models.IntegerField()  # Приоритет сортировки

    class Meta:
        unique_together = (
            "market",
            "unit",
        )  # Уникальная пара (рынок, единица измерения)
        ordering = ["priority"]  # Сортировка по приоритету

    def __str__(self):
        return f"{self.market.name} - {self.unit.name} (Priority: {self.priority})"
