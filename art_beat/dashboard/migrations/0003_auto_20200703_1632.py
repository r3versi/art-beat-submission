# Generated by Django 3.0.8 on 2020-07-03 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200703_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='confidence',
            field=models.FloatField(blank=True, null=True),
        ),
    ]