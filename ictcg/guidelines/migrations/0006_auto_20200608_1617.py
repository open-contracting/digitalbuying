# Generated by Django 3.0.5 on 2020-06-08 16:17

import wagtail.core.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("guidelines", "0005_auto_20200528_1422"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="guidelinessectionpage",
            name="sub_sections_title",
        ),
        migrations.AddField(
            model_name="guidelinessectionpage",
            name="introduction",
            field=wagtail.core.fields.RichTextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="guidelinessectionpage",
            name="body",
            field=wagtail.core.fields.RichTextField(blank=True, default=""),
        ),
    ]
