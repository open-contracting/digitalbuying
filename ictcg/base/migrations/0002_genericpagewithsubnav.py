# Generated by Django 3.0.5 on 2020-05-15 14:54

import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailtrans", "0009_create_initial_language"),
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GenericPageWithSubNav",
            fields=[
                (
                    "translatablepage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailtrans.TranslatablePage",
                    ),
                ),
                (
                    "navigation_title",
                    models.CharField(blank=True, help_text="Title for Navigation", max_length=120, null=True),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "rich_text_section",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.core.blocks.CharBlock(
                                                help_text="Section title, max length 120 characters", max_length=120
                                            ),
                                        ),
                                        ("content", wagtail.core.blocks.RichTextBlock()),
                                    ]
                                ),
                            ),
                            (
                                "quote_section",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.core.blocks.CharBlock(
                                                help_text="Quote section title, max length 120 characters",
                                                max_length=120,
                                            ),
                                        ),
                                        ("content_top", wagtail.core.blocks.RichTextBlock()),
                                        ("quote", wagtail.core.blocks.CharBlock(help_text="Quote", max_length=300)),
                                        (
                                            "attribution",
                                            wagtail.core.blocks.CharBlock(
                                                help_text="Quote attribution", max_length=120
                                            ),
                                        ),
                                        ("content_bottom", wagtail.core.blocks.RichTextBlock()),
                                    ]
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailtrans.translatablepage",),
        ),
    ]
