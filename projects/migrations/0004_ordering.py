# Generated by Django 4.2 on 2023-04-17 17:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_auto_increment_uuid"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["external_id"], "verbose_name": "Project", "verbose_name_plural": "Projects"},
        ),
    ]