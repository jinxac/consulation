# Generated by Django 3.0.3 on 2020-03-02 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_auto_20200302_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='date_of_birth',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='practicing_from',
            field=models.DateTimeField(blank=True),
        ),
    ]