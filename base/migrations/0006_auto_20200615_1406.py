# Generated by Django 3.0.5 on 2020-06-15 14:06

import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0005_auto_20200603_1556"),
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
                                ("quote", wagtail.core.blocks.CharBlock(help_text="Quote", max_length=300)),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(help_text="Quote attribution", max_length=120),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
