# Generated by Django 2.0.3 on 2018-04-03 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baggage_Recovery_App', '0002_report_potential_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_potential_bag',
            name='REPORT_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='REPORT_ID', to='Baggage_Recovery_App.REPORT'),
        ),
    ]
