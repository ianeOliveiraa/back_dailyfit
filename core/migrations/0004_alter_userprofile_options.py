# Generated by Django 5.1.3 on 2024-11-21 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_exercise_category_alter_exercise_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'managed': True, 'verbose_name': 'Perfil do usuário', 'verbose_name_plural': 'Perfis dos usuários'},
        ),
    ]
