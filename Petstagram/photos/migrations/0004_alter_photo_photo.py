# Generated by Django 5.0.4 on 2025-04-27 11:36

import Petstagram.photos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='photos/', validators=[Petstagram.photos.validators.validate_file_size]),
        ),
    ]
