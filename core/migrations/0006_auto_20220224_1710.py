# Generated by Django 3.2.10 on 2022-02-24 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_order_paid_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='accepted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
