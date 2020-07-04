# Generated by Django 3.0.8 on 2020-07-03 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200703_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='analyzed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='magnitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]