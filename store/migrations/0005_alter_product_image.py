# Generated by Django 4.2.7 on 2023-11-30 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.png', null=True, upload_to='images'),
        ),
    ]