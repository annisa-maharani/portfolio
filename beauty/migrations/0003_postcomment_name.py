# Generated by Django 3.2.7 on 2021-10-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0002_postcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]