# Generated by Django 3.1.6 on 2023-02-16 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0004_auto_20230216_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Owner's Author Id"),
        ),
        migrations.AlterField(
            model_name='post',
            name='host',
            field=models.URLField(help_text='The node that created the post', max_length=128),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.URLField(help_text='The node that shared the post', max_length=128),
        ),
        migrations.AlterField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False, help_text='Does this post appear in authors streams'),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('FRIENDS', 'Friends'), ('PUBLIC', 'Public')], help_text='Who can view this post', max_length=16),
        ),
    ]
