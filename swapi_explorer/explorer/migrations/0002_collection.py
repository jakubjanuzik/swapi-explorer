# Generated by Django 3.2.5 on 2021-07-04 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("explorer", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("csv_file", models.FileField(upload_to="csvs/")),
            ],
        )
    ]
