# Generated by Django 3.0.5 on 2021-08-02 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart_data', '0002_auto_20210802_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filehistory',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]