# Generated by Django 3.2.10 on 2022-02-22 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0008_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Nomor Telepon : '),
        ),
    ]
