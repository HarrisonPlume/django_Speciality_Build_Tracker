# Generated by Django 3.2.5 on 2021-07-07 22:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_componentpreptaskinstance_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique Part id for each task created', primary_key=True, serialize=False),
        ),
    ]
