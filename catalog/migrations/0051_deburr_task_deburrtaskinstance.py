# Generated by Django 3.2.5 on 2021-07-14 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0050_alter_part_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deburr_Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeburrTaskInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('a', 'Not Started'), ('h', 'On Hold'), ('c', 'Complete'), ('p', 'In Progress'), ('f', 'Failed')], default='a', help_text='Set task completion status', max_length=1)),
                ('part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.part')),
            ],
            options={
                'ordering': ['status'],
            },
        ),
    ]
