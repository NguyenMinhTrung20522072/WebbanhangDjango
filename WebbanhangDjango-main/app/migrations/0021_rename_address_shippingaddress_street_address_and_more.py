# Generated by Django 4.2.1 on 2023-06-01 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_product_features'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='street_address',
        ),
        migrations.AlterField(
            model_name='product',
            name='features',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]