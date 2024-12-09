from django.contrib import admin
from django.db.models import Sum

from core.models import MuscleGroup, Exercise, Training, UserProfile, TrainingExercise, Meal, MealFood, Food


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass


class TrainingExerciseAdmin(admin.TabularInline):
    model = TrainingExercise
    list_display = ['id', 'training', 'exercise', 'repetitions', 'series', 'rest_time']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [
        TrainingExerciseAdmin,
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'login', 'age', 'weight', 'height', 'active']


@admin.register(Food)
class MealAdmin(admin.ModelAdmin):
    pass


class MealFoodAdmin(admin.TabularInline):
    model = MealFood


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    inlines = [
        MealFoodAdmin,
    ]
    list_display = ['id', 'meal_type', 'total']

    def total(self, obj):
        meal_foods = MealFood.objects.filter(meal=obj)  # .aggregate(total_calories=Sum('nb_value'))['total_calories']
        resultado = 0

        for meal_food in meal_foods:
            if meal_food.value <= 0 or meal_food.food.value <= 0:
                continue
            total_food = (meal_food.value / meal_food.food.value) * meal_food.food.total_kcal
            resultado += total_food

        return resultado

    total.short_description = 'Total de Calorias'
