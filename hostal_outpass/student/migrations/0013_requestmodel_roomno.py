# Generated by Django 4.1 on 2024-09-13 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_alter_requestmodel_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmodel',
            name='roomNo',
            field=models.IntegerField(null=True),
        ),
    ]