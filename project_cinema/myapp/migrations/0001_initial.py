# Generated by Django 2.1.15 on 2023-08-03 22:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acteurs_films',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acteurs', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'acteurs_films',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=500)),
                ('distributeur', models.CharField(max_length=500)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('type_film', models.CharField(default='Unknown', max_length=100)),
            ],
            options={
                'db_table': 'films',
            },
        ),
        migrations.AddField(
            model_name='acteurs_films',
            name='film_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Film'),
        ),
    ]