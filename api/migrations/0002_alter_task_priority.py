# Generated by Django 4.0.4 on 2022-09-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Urgent', 'Urgent')], default='Low', max_length=6),
        ),
    ]
