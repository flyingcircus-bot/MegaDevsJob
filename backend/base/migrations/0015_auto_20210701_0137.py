# Generated by Django 3.2.4 on 2021-06-30 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_apply_paidat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='isDelivered',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='apply',
            name='paidAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
