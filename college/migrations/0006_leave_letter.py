# Generated by Django 4.2.2 on 2024-03-22 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('college', '0005_delete_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='leave_letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Sick Leave', 'Sick Leave'), ('Parental Leave:', 'Parental Leave:'), ('Educational Leave', 'Educational Leave'), ('Religious Observance Leave', 'Religious Observance Leave'), ('Family Event Leave', 'Family Event Leave')], max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.staff')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
