# Generated by Django 3.1.2 on 2020-10-10 20:12

from django.db import migrations, models
import piclab.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201004_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=piclab.api.models.upload_path),
        ),
    ]
