# Generated by Django 4.2.4 on 2023-10-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]