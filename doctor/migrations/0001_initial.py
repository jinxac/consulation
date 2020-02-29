# Generated by Django 3.0.2 on 2020-02-29 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_removed', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('professional_statement', models.CharField(blank=True, max_length=300, null=True)),
                ('practicing_from', models.DateField()),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_removed', models.DateTimeField(blank=True, null=True)),
                ('specialization_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_removed', models.DateTimeField(blank=True, null=True)),
                ('qualification_name', models.CharField(max_length=100)),
                ('institute_name', models.CharField(max_length=100)),
                ('procurement_year', models.DateField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.Doctor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_removed', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.Doctor')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.Specialization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='doctor',
            name='specializations',
            field=models.ManyToManyField(through='doctor.DoctorSpecialization', to='doctor.Specialization'),
        ),
    ]
