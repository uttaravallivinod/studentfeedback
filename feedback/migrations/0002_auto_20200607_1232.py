# Generated by Django 2.2.10 on 2020-06-07 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='college',
            old_name='college',
            new_name='name',
        ),
    ]
