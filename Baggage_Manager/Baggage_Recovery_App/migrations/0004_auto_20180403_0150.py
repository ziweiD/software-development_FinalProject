# Generated by Django 2.0.3 on 2018-04-03 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baggage_Recovery_App', '0003_report_potential_bag_report_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_potential_bag',
            name='NUM',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
