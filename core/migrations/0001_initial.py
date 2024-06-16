# Generated by Django 5.0.6 on 2024-06-15 15:48

import django_extensions.db.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('telephone', models.CharField(max_length=20)),
                ('message', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'contacts via web site',
            },
        ),
    ]