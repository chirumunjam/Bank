# Generated by Django 5.1.5 on 2025-02-05 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_no', models.PositiveBigIntegerField(auto_created=True, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.PositiveBigIntegerField()),
                ('email', models.EmailField(max_length=50)),
                ('aadhar', models.PositiveBigIntegerField()),
                ('father_name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=1000)),
                ('balance', models.PositiveIntegerField(default=500)),
                ('pin', models.IntegerField(blank=True)),
                ('photo', models.ImageField(upload_to='profile_pics/')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gender')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.state')),
            ],
        ),
    ]
