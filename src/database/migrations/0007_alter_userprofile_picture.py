# Generated by Django 4.2.14 on 2024-07-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "database",
            "0006_alter_application_picture_alter_application_resume_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="picture",
            field=models.FileField(
                blank=True, null=True, upload_to="user_profile_pictures"
            ),
        ),
    ]
