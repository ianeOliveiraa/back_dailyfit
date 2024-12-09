from django_filters import rest_framework as filters
from core import models



from django_filters import rest_framework as filters
from core import models
from core.choices import MEALS


class TrainingFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='unaccent__icontains')

    class Meta:
        model = models.Training
        fields = ['name']


class MealFilter(filters.FilterSet):
    meal_type_label = filters.CharFilter(method='filter_by_label')
    date = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = models.Meal
        fields = ['meal_type_label', 'date']

    def filter_by_label(self, queryset, name, value):
        # Cria um dicionário para mapear rótulos para valores
        meal_type_map = {label: key for key, label in MEALS}

        # Busca o valor correspondente ao rótulo fornecido
        meal_type_value = meal_type_map.get(value)
        if meal_type_value is not None:
            return queryset.filter(meal_type=meal_type_value)
        return queryset.none()

