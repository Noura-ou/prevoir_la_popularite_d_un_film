# Generated by Django 2.1.15 on 2023-08-10 10:37

from django.db import migrations, models
import django.db.models.deletion


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
                'db_table': 'actors',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=500)),
                ('distributeur', models.CharField(max_length=500)),
                ('type_film', models.CharField(default='Unknown', max_length=100)),
            ],
            options={
                'db_table': 'dataset_model_ML',
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=500)),
                ('image', models.URLField()),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction', models.FloatField()),
                ('titre', models.CharField(max_length=500)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Movies')),
            ],
            options={
                'db_table': 'prediction',
            },
        ),
        migrations.AddField(
            model_name='acteurs_films',
            name='film_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Film'),
        ),
    ]
