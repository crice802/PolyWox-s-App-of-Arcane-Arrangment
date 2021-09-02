# Generated by Django 3.2.6 on 2021-09-02 21:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('char_class', models.CharField(choices=[('barbarian', 'barbarian'), ('bard', 'bard'), ('cleric', 'cleric'), ('druid', 'druid'), ('fighter', 'fighter'), ('monk', 'monk'), ('paladin', 'paladin'), ('ranger', 'ranger'), ('rogue', 'rogue'), ('sorcerer', 'sorcerer'), ('warlock', 'warlock'), ('wizard', 'wizard')], default='barbarian', max_length=9)),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)])),
                ('spell_list', models.CharField(max_length=10000)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=10000)),
                ('level', models.IntegerField()),
                ('higher_level', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.character')),
            ],
        ),
    ]