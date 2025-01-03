# Generated by Django 5.0.6 on 2024-09-07 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('register_number', models.BigIntegerField(unique=True)),
                ('department', models.CharField(max_length=150)),
                ('district', models.CharField(max_length=100)),
                ('phone_number', models.BigIntegerField()),
                ('parent_number', models.BigIntegerField(null=True)),
                ('year', models.PositiveSmallIntegerField(choices=[(1, 'first_year'), (2, 'second_year'), (3, 'thir_year'), (4, 'final_year')], null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.BigIntegerField()),
                ('regNo', models.BigIntegerField()),
                ('phone_number', models.BigIntegerField()),
                ('name', models.CharField(max_length=150)),
                ('purpose', models.CharField(max_length=150)),
                ('inTime', models.DateTimeField()),
                ('outTime', models.DateTimeField()),
                ('pending', models.PositiveSmallIntegerField(choices=[('pending', 1), ('accept', 2), ('reject', 3)], default=1, help_text='1-pending, 2-accept, 3-reject')),
            ],
        ),
    ]
