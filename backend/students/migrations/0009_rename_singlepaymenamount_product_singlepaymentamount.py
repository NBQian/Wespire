# Generated by Django 5.0.2 on 2024-03-14 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_rename_yearly_product_yearlypaymentamount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='SinglePaymenAmount',
            new_name='SinglePaymentAmount',
        ),
    ]
