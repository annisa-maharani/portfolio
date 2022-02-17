# Generated by Django 3.2.8 on 2022-02-17 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beauty', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_link', models.SlugField(max_length=255)),
                ('post_code', models.CharField(max_length=255)),
                ('main_address', models.TextField()),
                ('detailed_address', models.CharField(max_length=255)),
                ('default', models.BooleanField(default=False)),
                ('mark_as', models.CharField(choices=[('R', 'Rumah'), ('K', 'Kantor')], default='R', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]