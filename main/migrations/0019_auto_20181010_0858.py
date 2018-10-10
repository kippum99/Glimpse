# Generated by Django 2.1.1 on 2018-10-10 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='submitted_videos',
            field=models.ManyToManyField(related_name='submitted_to', through='main.Submission', to='main.Video'),
        ),
        migrations.AlterField(
            model_name='video',
            name='submitted_videos1',
            field=models.ManyToManyField(related_name='submitted_too', to='main.Video'),
        ),
    ]
