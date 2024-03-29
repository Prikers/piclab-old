# Generated by Django 3.1.2 on 2020-10-04 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201004_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-date_created']},
        ),
        migrations.RemoveField(
            model_name='photo',
            name='date',
        ),
        migrations.AddField(
            model_name='photo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
