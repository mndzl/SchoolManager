# Generated by Django 3.0.3 on 2020-04-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='delegate',
            field=models.BooleanField(default=False),
        ),
    ]