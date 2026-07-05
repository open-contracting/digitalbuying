# Phase 4a of migrating off wagtailtrans: add a direct page_ptr parent link to
# wagtailcore.Page alongside translatablepage_ptr, copying the (equal) id.
import django.db.models.deletion
from django.db import migrations, models


def copy_page_ptr(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for table in (
            "guidelines_guidancepage",
            "guidelines_guidelineslistingpage",
            "guidelines_guidelinessectionpage",
        ):
            cursor.execute(f"UPDATE {table} SET page_ptr_id = translatablepage_ptr_id")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("guidelines", "0009_guidancepage_information_banners"),
    ]

    operations = [
        migrations.AddField(
            model_name="guidancepage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True,
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="guidelineslistingpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True,
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="guidelinessectionpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True,
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.RunPython(copy_page_ptr, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="guidancepage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
        migrations.AlterField(
            model_name="guidelineslistingpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
        migrations.AlterField(
            model_name="guidelinessectionpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
    ]
