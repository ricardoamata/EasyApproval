# Generated by Django 3.0 on 2019-12-06 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191206_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='duracion',
            field=models.SmallIntegerField(),
        ),
    ]