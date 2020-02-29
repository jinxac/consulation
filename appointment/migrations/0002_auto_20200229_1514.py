# Generated by Django 3.0.2 on 2020-02-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('appointment', '0001_initial'),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office.Office'),
        ),
    ]
