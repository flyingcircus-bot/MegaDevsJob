# Generated by Django 3.2.4 on 2021-06-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='shippingPrice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apply',
            name='taxPrice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apply',
            name='totalPrice',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
