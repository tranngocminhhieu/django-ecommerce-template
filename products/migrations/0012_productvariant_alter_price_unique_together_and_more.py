# Generated by Django 4.2.4 on 2023-10-18 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_orderitem_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='price',
            name='product',
        ),
        migrations.RemoveField(
            model_name='price',
            name='product_color',
        ),
        migrations.RemoveField(
            model_name='price',
            name='version',
        ),
        migrations.AlterUniqueTogether(
            name='productcolor',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='productcolor',
            name='color',
        ),
        migrations.RemoveField(
            model_name='productcolor',
            name='product',
        ),
        migrations.RemoveField(
            model_name='version',
            name='description',
        ),
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='color',
            unique_together={('product', 'name')},
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.DeleteModel(
            name='ProductColor',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.color'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.version'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='review',
            name='product_variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='products.productvariant'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('product_variant', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'color', 'version')},
        ),
        migrations.RemoveField(
            model_name='review',
            name='cons',
        ),
        migrations.RemoveField(
            model_name='review',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='review',
            name='like',
        ),
        migrations.RemoveField(
            model_name='review',
            name='product',
        ),
        migrations.RemoveField(
            model_name='review',
            name='pros',
        ),
    ]