# Generated by Django 5.1.3 on 2025-01-29 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EndUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0)),
                ('is_portal_admin', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=255)),
                ('shipping_address', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
