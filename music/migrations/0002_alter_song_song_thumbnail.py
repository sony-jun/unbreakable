# Generated by Django 3.2.13 on 2022-12-01 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_thumbnail',
            field=models.CharField(default=1, max_length=400),
            preserve_default=False,
        ),
    ]
