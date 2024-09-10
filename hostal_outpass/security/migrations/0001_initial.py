# Generated by Django 5.1 on 2024-09-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='securityLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
                ('phone_number', models.BigIntegerField(verbose_name='security_phone_number')),
            ],
        ),
    ]
