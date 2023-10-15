# Generated by Django 4.2.4 on 2023-10-14 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_gallery_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='youtube_embed',
            new_name='youtube',
        ),
        migrations.AlterUniqueTogether(
            name='gallery',
            unique_together={('media_type', 'image', 'youtube', 'product')},
        ),
    ]
