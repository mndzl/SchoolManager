# Generated by Django 3.0.3 on 2020-04-10 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('task', '0002_auto_20200408_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='grade',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.Grade'),
        ),
    ]
