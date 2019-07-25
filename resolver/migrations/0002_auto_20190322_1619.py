# Generated by Django 2.0.3 on 2019-03-22 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0004_auto_20180405_2237'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resolver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='images', to='albums.Album'),
        ),
        migrations.AddField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='image',
            name='message',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='message_html',
            field=models.TextField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='images', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
