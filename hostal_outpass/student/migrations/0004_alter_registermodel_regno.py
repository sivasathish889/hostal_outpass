# Generated by Django 5.0.6 on 2024-08-30 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_registermodel_dept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='regNo',
            field=models.BigIntegerField(unique=True),
        ),
    ]
