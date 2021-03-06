# Generated by Django 3.2.5 on 2021-07-07 22:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_part_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 8, 8, 22, 54, 758874), verbose_name='time published'),
        ),
        migrations.AlterField(
            model_name='part',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
