# Generated by Django 4.2.11 on 2024-04-05 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0008_circular'),
    ]

    operations = [
        migrations.CreateModel(
            name='circulars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('message', models.TextField(blank=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.department')),
            ],
        ),
        migrations.DeleteModel(
            name='circular',
        ),
    ]
