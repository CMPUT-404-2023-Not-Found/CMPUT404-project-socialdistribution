# Generated by Django 3.2.18 on 2023-03-28 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0003_auto_20230326_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='display_name',
            field=models.CharField(default='', max_length=128),
        ),
    ]