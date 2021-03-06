# Generated by Django 3.2.5 on 2021-10-31 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0089_alter_stackingtaskinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='priority',
            field=models.IntegerField(default=30, help_text='                                            Select the nessessary priority                                                ', null=True),
        ),
        migrations.AlterField(
            model_name='wirecuttaskinstance',
            name='status',
            field=models.IntegerField(choices=[(2, 'Not Started'), (3, 'On Hold'), (10, 'Complete'), (1, 'In Progress')], default=2, help_text='Set task completion status', max_length=1),
        ),
    ]
