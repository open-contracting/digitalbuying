# Phase 4a of migrating off wagtailtrans: add a direct page_ptr parent link to
# wagtailcore.Page alongside the existing translatablepage_ptr, copying the id
# (they are equal — MTI shares the primary key). translatablepage_ptr is dropped
# in the following migration once the models no longer inherit TranslatablePage.
import django.db.models.deletion
from django.db import migrations, models


def copy_page_ptr(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("UPDATE base_genericpage SET page_ptr_id = translatablepage_ptr_id")
        cursor.execute("UPDATE base_genericpagewithsubnav SET page_ptr_id = translatablepage_ptr_id")
        cursor.execute("UPDATE base_homepage SET page_ptr_id = translatablepage_ptr_id")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("base", "0011_auto_20250108_0602"),
    ]

    operations = [
        migrations.AddField(
            model_name="genericpage",
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
            model_name="genericpagewithsubnav",
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
            model_name="homepage",
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
            model_name="genericpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
        migrations.AlterField(
            model_name="genericpagewithsubnav",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
    ]
