# Generated by Django 2.0.5 on 2018-05-10 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180509_0500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='text',
            new_name='name',
        ),
    ]
