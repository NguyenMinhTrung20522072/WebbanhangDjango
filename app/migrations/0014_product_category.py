# Generated by Django 4.2.1 on 2023-05-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_product_category_category_is_sub_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='app.category'),
        ),
    ]
