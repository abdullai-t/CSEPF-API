# Generated by Django 4.2.14 on 2024-07-20 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_alter_userprofile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AddField(
            model_name='fellow',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
