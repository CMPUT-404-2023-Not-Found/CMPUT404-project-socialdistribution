# Generated by Django 3.2.18 on 2023-03-19 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_category_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
