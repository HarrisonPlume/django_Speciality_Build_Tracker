# Generated by Django 3.2.5 on 2021-10-28 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0079_auto_20211028_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componentpreptaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='deburrtaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='formingtaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='headerplatetaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='pitchingtaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='platingtaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='stackingtaskinstance',
            options={'ordering': ['part', 'status']},
        ),
        migrations.AlterModelOptions(
            name='wirecuttaskinstance',
            options={'ordering': ['part', 'status']},
        ),
    ]
