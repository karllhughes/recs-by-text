# Generated by Django 2.2.4 on 2019-09-08 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviesImporter', '0004_auto_20190824_2101'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION fuzzystrmatch"
        )
    ]
