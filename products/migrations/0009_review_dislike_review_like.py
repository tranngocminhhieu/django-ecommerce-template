# Generated by Django 4.2.4 on 2023-10-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_youtube_embed_gallery_youtube_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='dislike',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
