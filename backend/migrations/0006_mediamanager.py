# Generated by Django 3.2.7 on 2021-09-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_remove_socialmedia_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='manager/')),
            ],
        ),
    ]
