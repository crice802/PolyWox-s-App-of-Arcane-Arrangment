# Generated by Django 3.2.6 on 2021-09-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210905_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='spell_list',
            field=models.ManyToManyField(blank=True, to='main_app.Spell'),
        ),
    ]
