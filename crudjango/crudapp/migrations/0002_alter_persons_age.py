# Generated by Django 5.1.2 on 2024-10-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='age',
            field=models.IntegerField(),
        ),
    ]
