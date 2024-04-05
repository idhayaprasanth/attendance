# Generated by Django 4.2.2 on 2024-03-10 14:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd')], max_length=3)),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J')], max_length=1)),
                ('subject1', models.CharField(max_length=100, null=True)),
                ('subject2', models.CharField(max_length=100, null=True)),
                ('subject3', models.CharField(max_length=100, null=True)),
                ('subject4', models.CharField(max_length=100, null=True)),
                ('subject5', models.CharField(max_length=100, null=True)),
                ('subject6', models.CharField(max_length=100, null=True)),
                ('subject7', models.CharField(max_length=100, null=True)),
                ('subject8', models.CharField(max_length=100, null=True)),
                ('subject9', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg', models.SlugField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6, null=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.classroom')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.department')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.staff')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.department'),
        ),
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=datetime.date.today)),
                ('hour_1_present', models.BooleanField(default=False, null=True)),
                ('hour_2_present', models.BooleanField(default=False, null=True)),
                ('hour_3_present', models.BooleanField(default=False, null=True)),
                ('hour_4_present', models.BooleanField(default=False, null=True)),
                ('hour_5_present', models.BooleanField(default=False, null=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.student')),
            ],
        ),
    ]
