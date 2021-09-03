# Generated by Django 3.2.6 on 2021-09-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='spell_list',
        ),
        migrations.AddField(
            model_name='character',
            name='spell_list',
            field=models.ManyToManyField(blank=True, null=True, to='main_app.Spell'),
        ),
    ]
