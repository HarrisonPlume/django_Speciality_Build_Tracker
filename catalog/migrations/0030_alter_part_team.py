# Generated by Django 3.2.5 on 2021-07-08 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_alter_team_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.team'),
        ),
    ]
