# Generated by Django 4.2.11 on 2024-03-19 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_path', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=250, unique_for_date='uploaded_at')),
                ('video_file', models.FileField(upload_to='videos/')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('PB', 'Public'), ('PR', 'Private')], default='PB', max_length=2)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_videos', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
