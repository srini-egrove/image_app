# Generated by Django 4.2 on 2023-04-20 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='file',
        ),
    ]
