# Generated by Django 3.2.10 on 2022-03-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_shipping_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paid_at',
        ),
        migrations.AlterField(
            model_name='order',
            name='reff',
            field=models.SlugField(blank=True, default='', max_length=255, null=True),
        ),
    ]
