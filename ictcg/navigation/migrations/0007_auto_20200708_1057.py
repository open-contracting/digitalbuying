# Generated by Django 3.0.5 on 2020-07-08 10:57

import django.db.models.deletion
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("navigation", "0006_auto_20200623_0914"),
    ]

    operations = [
        migrations.AddField(
            model_name="mainmenu",
            name="cookie_banner_button_text",
            field=models.CharField(help_text="Text for cookie accept button", max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="mainmenu",
            name="cookie_banner_description",
            field=wagtail.core.fields.RichTextField(
                blank=True, default="", help_text="Text area for cookie banner description"
            ),
        ),
        migrations.AddField(
            model_name="mainmenu",
            name="cookie_banner_preferences_link_text",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="mainmenu",
            name="cookie_banner_title",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="mainmenu",
            name="cookie_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.Page",
            ),
        ),
    ]
