# Generated by Django 3.2.4 on 2021-07-01 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_manageinfo_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manageinfo',
            old_name='image',
            new_name='imagee',
        ),
    ]
