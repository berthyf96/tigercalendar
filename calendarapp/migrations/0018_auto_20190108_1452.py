# Generated by Django 2.1.2 on 2019-01-08 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0017_auto_20190108_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
