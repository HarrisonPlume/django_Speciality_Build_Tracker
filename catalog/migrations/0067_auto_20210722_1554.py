# Generated by Django 3.2.5 on 2021-07-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0066_auto_20210722_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='createtime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='createtimenum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='finishtime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='starttime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='starttimenum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='timetaken',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wirecuttaskinstance',
            name='timetostart',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
