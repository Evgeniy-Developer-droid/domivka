# Generated by Django 4.0.4 on 2022-05-15 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_realestate_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_districts', models.BooleanField(default=False)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('radius', models.IntegerField(default=1)),
                ('zoom', models.IntegerField(default=1)),
                ('name', models.CharField(max_length=255)),
                ('normalized_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('normalized_name', models.CharField(max_length=255)),
            ],
        ),
    ]