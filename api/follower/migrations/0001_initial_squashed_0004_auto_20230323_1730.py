# Generated by Django 3.2.18 on 2023-03-23 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('follower', '0001_initial'), ('follower', '0002_auto_20230314_2052'), ('follower', '0003_alter_follower_follower'), ('follower', '0004_auto_20230323_1730')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('follower', models.URLField(db_index=True, max_length=128, verbose_name='author who is following the followee')),
                ('followed_at', models.DateTimeField(auto_now_add=True, verbose_name='Followed At')),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee', to=settings.AUTH_USER_MODEL)),
                ('id', models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'unique_together': {('follower', 'followee')},
            },
        ),
    ]
