# Generated by Django 3.2.5 on 2021-10-28 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0076_auto_20210922_1646'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ['priority', 'title', 'serial']},
        ),
        migrations.AddField(
            model_name='part',
            name='priority',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
