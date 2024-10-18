from rest_framework import serializers
from .models import Market, Unit, MarketUnitPriority


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name"]  # Указываем поля, которые хотим сериализовать


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name"]  # Указываем поля, которые хотим сериализовать


class MarketUnitPrioritySerializer(serializers.ModelSerializer):
    market = MarketSerializer()  # Вложенный сериализатор для рынка
    unit = UnitSerializer()  # Вложенный сериализатор для единицы измерения

    class Meta:
        model = MarketUnitPriority
        fields = ["id", "market", "unit", "priority"]  # Указываем поля для сериализации

    def create(self, validated_data):
        market_data = validated_data.pop("market")
        unit_data = validated_data.pop("unit")

        market, created = Market.objects.get_or_create(**market_data)
        unit, created = Unit.objects.get_or_create(**unit_data)

        market_unit_priority = MarketUnitPriority.objects.create(
            market=market, unit=unit, **validated_data
        )
        return market_unit_priority

    def update(self, instance, validated_data):
        market_data = validated_data.pop("market")
        unit_data = validated_data.pop("unit")

        instance.priority = validated_data.get("priority", instance.priority)

        # Обновляем или создаем рынок и единицу измерения
        market, created = Market.objects.get_or_create(**market_data)
        unit, created = Unit.objects.get_or_create(**unit_data)

        instance.market = market
        instance.unit = unit
        instance.save()

        return instance
