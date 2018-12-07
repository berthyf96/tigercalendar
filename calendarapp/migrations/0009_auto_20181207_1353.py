# Generated by Django 2.1.2 on 2018-12-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0008_auto_20181207_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netid', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='favorite_users',
        ),
        migrations.AddField(
            model_name='event',
            name='favorite_users',
            field=models.ManyToManyField(to='calendarapp.User'),
        ),
    ]
