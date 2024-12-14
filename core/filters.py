
from django_filters import rest_framework as filters
from core import models

class TrainingFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='unaccent__icontains')

    class Meta:
        model = models.Training
        fields = ['name']




