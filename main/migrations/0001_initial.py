# Generated by Django 4.2.7 on 2023-11-24 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Site",
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
                ("name", models.CharField(max_length=63, unique=True)),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Statistic",
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
                ("page_views", models.PositiveIntegerField(default=0)),
                ("data_sent", models.PositiveIntegerField(default=0)),
                ("data_received", models.PositiveIntegerField(default=0)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections",
                        to="main.site",
                    ),
                ),
            ],
        ),
    ]
