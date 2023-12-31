# Generated by Django 4.2.4 on 2023-09-10 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_content_post_time_to_read_postlikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='time_to_read',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
