# Generated by Django 5.0.2 on 2024-04-15 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_remove_product_endowment_remove_product_invlinked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='BasicSumAssured',
        ),
        migrations.AddField(
            model_name='product',
            name='BasicSum',
            field=models.DecimalField(decimal_places=2, default=7000, max_digits=14),
            preserve_default=False,
        ),
    ]
