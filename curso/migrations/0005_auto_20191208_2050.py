# Generated by Django 2.2.7 on 2019-12-09 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0004_auto_20191208_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='nombre',
            field=models.CharField(max_length=40),
        ),
    ]