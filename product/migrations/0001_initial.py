# Generated by Django 4.0.4 on 2022-06-03 16:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.UUID('67556d88-d58a-4a62-836d-bd1ef17fb6d0'), editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('selling_price', models.CharField(blank=True, max_length=20, null=True)),
                ('desc', models.CharField(max_length=500)),
                ('feature_img', models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.UUID('67556d88-d58a-4a62-836d-bd1ef17fb6d0'), editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
