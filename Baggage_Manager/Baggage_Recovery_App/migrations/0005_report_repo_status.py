# Generated by Django 2.0.3 on 2018-04-06 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baggage_Recovery_App', '0004_auto_20180403_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='REPO_STATUS',
            field=models.IntegerField(default=0),
        ),
    ]
