# Generated by Django 4.2.4 on 2023-09-21 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_slug_alter_post_time_to_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post'),
        ),
    ]
