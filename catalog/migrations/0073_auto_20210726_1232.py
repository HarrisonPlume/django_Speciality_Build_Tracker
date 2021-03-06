# Generated by Django 3.2.5 on 2021-07-26 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0072_auto_20210726_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='Component_Prep_tasks',
            field=models.ManyToManyField(blank=True, help_text='Select                                      the component prep tasks                                          to be completed.', to='catalog.Component_Prep_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Deburr_tasks',
            field=models.ManyToManyField(blank=True, help_text='                                            Select the nessessary deburr                                                tasks', to='catalog.Deburr_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Forming_tasks',
            field=models.ManyToManyField(blank=True, help_text='Select                                           the required forming tasks.', to='catalog.Forming_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Header_Plate_tasks',
            field=models.ManyToManyField(blank=True, help_text='                                                Select The nessessary header                                                     plate tasks', to='catalog.Header_Plate_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Pitching_tasks',
            field=models.ManyToManyField(blank=True, help_text='                                            Select the nessessary pitching                                                 tasks', to='catalog.Pitching_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Plating_tasks',
            field=models.ManyToManyField(blank=True, help_text='                                            Select the nessessary plating                                                tasks', to='catalog.Plating_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Stacking_tasks',
            field=models.ManyToManyField(blank=True, help_text='Select                                         the required stacking tasks.', to='catalog.Stacking_Task'),
        ),
        migrations.AlterField(
            model_name='part',
            name='Wire_Cut_tasks',
            field=models.ManyToManyField(blank=True, help_text='                                            Select the nessessary wire cut                                                tasks', to='catalog.Wire_Cut_Task'),
        ),
    ]
