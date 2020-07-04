# Generated by Django 3.0.8 on 2020-07-04 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20200703_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='room',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='y',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]