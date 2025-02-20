# Generated by Django 3.0.5 on 2020-05-28 14:22

import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_homepage_masthead_image_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genericpagewithsubnav",
            name="body",
            field=wagtail.core.fields.StreamField(
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
                                ("hide_horizontal_rule", wagtail.core.blocks.BooleanBlock(required=False)),
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
                                        help_text="Quote section title, max length 120 characters", max_length=120
                                    ),
                                ),
                                ("hide_horizontal_rule", wagtail.core.blocks.BooleanBlock(required=False)),
                                ("content_top", wagtail.core.blocks.RichTextBlock()),
                                ("quote", wagtail.core.blocks.CharBlock(help_text="Quote", max_length=300)),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(help_text="Quote attribution", max_length=120),
                                ),
                                ("content_bottom", wagtail.core.blocks.RichTextBlock(required=False)),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "content_section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Section title, max length 120 characters", max_length=120
                                    ),
                                ),
                                ("hide_horizontal_rule", wagtail.core.blocks.BooleanBlock(required=False)),
                                ("content", wagtail.core.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
