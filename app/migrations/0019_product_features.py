# Generated by Django 4.2.1 on 2023-05-31 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_product_description4'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]