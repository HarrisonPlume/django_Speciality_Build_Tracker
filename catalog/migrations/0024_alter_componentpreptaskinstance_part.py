# Generated by Django 3.2.5 on 2021-07-07 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_alter_componentpreptaskinstance_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentpreptaskinstance',
            name='part',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
