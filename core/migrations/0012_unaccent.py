# Generated by Django 5.1.3 on 2024-12-06 13:44


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_mealfood_unit_food_unit_food_value'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS unaccent;"),
    ]

