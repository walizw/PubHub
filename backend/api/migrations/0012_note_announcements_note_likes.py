# Generated by Django 4.1.7 on 2023-04-12 00:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_alter_activity_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="announcements",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="note",
            name="likes",
            field=models.IntegerField(default=0),
        ),
    ]
