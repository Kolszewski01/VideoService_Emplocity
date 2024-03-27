# Generated by Django 5.0.2 on 2024-03-26 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_name', models.CharField(max_length=255)),
                ('frame_url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frameApp.frame')),
            ],
        ),
    ]
