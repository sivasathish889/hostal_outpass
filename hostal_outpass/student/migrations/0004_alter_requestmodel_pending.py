# Generated by Django 5.0.6 on 2024-09-08 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_requestmodel_pending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='pending',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Rejected')], default=1, null=True),
        ),
    ]
