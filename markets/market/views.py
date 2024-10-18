from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from .models import MarketUnitPriority, Unit
from .serializers import UnitSerializer


def index(request):
    return HttpResponse("<h2>API Материалы и заказы</h2>")


class UnitListView(generics.ListAPIView):
    """
    API-представление для получения списка единиц измерения по идентификатору рынка.
    Сортировка осуществляется на основе приоритета из модели MarketUnitPriority.
    """

    serializer_class = UnitSerializer

    def get_queryset(self, id: int):
        """
        Переопределяем метод get_queryset для фильтрации единиц измерения
        по идентификатору рынка и сортировки по приоритету.
        """
        # Получаем приоритеты единиц измерения для указанного рынка
        try:
            market_units = MarketUnitPriority.objects.filter(
                market_id=id
            ).select_related("unit")
        except MarketUnitPriority.DoesNotExist:
            raise NotFound("Рынок с таким идентификатором не найден.")

        # Извлекаем уникальные единицы измерения и сортируем по приоритету
        units = [market_unit.unit for market_unit in market_units]
        return sorted(
            units,
            key=lambda x: next(
                (mu.priority for mu in market_units if mu.unit == x), float("inf")
            ),
        )

    def get(self, request, id: int):
        """
        Обрабатываем GET-запросы.
        Возвращаем список единиц измерения в формате JSON.
        """
        queryset = self.get_queryset(id)

        # Сериализуем данные
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
