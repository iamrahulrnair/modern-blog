# Generated by Django 4.2.4 on 2023-08-28 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
