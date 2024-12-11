from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from core import choices


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        null=True,
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
        null=True,
    )
    active = models.BooleanField(
        db_column='cs_active',
        null=True,
        default=True
    )

    class Meta:
        abstract = True
        managed = True


class UserProfile(ModelBase):
    login = models.ForeignKey(
        User,
        db_column='tx_user',
        on_delete=models.CASCADE,
        null=False
    )
    age = models.IntegerField(
        db_column='nb_age',
        null=False,
    )
    weight = models.FloatField(
        db_column='nb_weight',
        null=False,
    )
    height = models.FloatField(
        db_column='nb_height',
        null=False,
    )

    class Meta:
        managed = True
        db_table = 'user_profile'
        verbose_name = 'Perfil do usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self):
        return self.login.username


class MuscleGroup(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        max_length=70,
    )

    class Meta:
        managed = True
        db_table = 'muscle_group'
        verbose_name = "Grupo muscular"
        verbose_name_plural = "Grupos musculares"

    def __str__(self):
        return self.name


class Exercise(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        max_length=70,
        null=False,
    )

    muscle_group = models.ForeignKey(
        MuscleGroup,
        db_column='tx_muscle_group',
        on_delete=models.CASCADE,
    )

    class Meta:
        managed = True
        db_table = 'exercise'
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"

    def __str__(self):
        return self.name


class Training(ModelBase):
    user = models.ForeignKey(
        User,
        db_column='nb_user',
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(
        db_column='tx_name',
        max_length=70,
        null=False,
    )
    date = models.DateField(
        db_column='date',
        null=False,
        default=None
    )

    class Meta:
        managed = True
        db_table = 'training'


class TrainingExercise(ModelBase):
    exercise = models.ForeignKey(
        Exercise,
        db_column='tx_exercise',
        on_delete=models.CASCADE,
    )
    training = models.ForeignKey(
        Training,
        db_column='tx_training',
        on_delete=models.CASCADE,
    )
    repetitions = models.IntegerField(
        db_column='nb_repetitions',
        null=False,
    )
    series = models.IntegerField(
        db_column='nb_series',
        null=False,
    )
    rest_time = models.DurationField(
        db_column='nb_rest_time',
        null=False,
    )

    class Meta:
        managed = True
        db_table = 'training_exercise'


class Food(ModelBase):
    description = models.CharField(
        db_column='tx_name',
        null=False,
        max_length=300,
    )
    total_kcal = models.FloatField(
        db_column='nb_total_kcal',
    )
    unit = models.IntegerField(
        choices=choices.UNIT_MEASUREMENT,
        default=choices.GRAM
    )
    value = models.FloatField(
        db_column='nb_value',
        default=0
    )
    class Meta:
        db_table = 'food'
        verbose_name = "Comida"
        verbose_name_plural = "Comidas"

    def __str__(self):
        return self.description

class Meal(ModelBase):
    user = models.ForeignKey(
        User,
        db_column='nb_user',
        on_delete=models.CASCADE,
        null=False
    )
    date = models.DateField(
        db_column='tx_date',
        null=False,
    )
    meal_type = models.IntegerField(
        choices=choices.MEALS,
    )
    class Meta:
        managed = True
        db_table = 'meal'
        verbose_name = "Refeição"
        verbose_name_plural = "Refeições"

    def __str__(self):
        return f"{self.user.username} -  {self.date}"


class MealFood(ModelBase):
    meal = models.ForeignKey(
        Meal,
        db_column='nb_meal',
        on_delete=models.CASCADE,
    )
    food = models.ForeignKey(
        Food,
        db_column='nb_food',
        on_delete=models.CASCADE,
    )
    value = models.FloatField(
        db_column='nb_value',
    )
    class Meta:
        db_table = 'meal_food'
