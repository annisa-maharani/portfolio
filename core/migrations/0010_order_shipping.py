# Generated by Django 3.2.10 on 2022-02-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shipping'),
        ),
    ]