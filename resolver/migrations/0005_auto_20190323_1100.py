# Generated by Django 2.0.3 on 2019-03-23 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resolver', '0004_auto_20190323_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='message',
        ),
        migrations.RemoveField(
            model_name='image',
            name='message_html',
        ),
    ]
