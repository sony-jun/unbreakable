# Generated by Django 3.2.13 on 2022-12-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='music_start',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='articles',
            name='music_url',
            field=models.TextField(null=True),
        ),
    ]
