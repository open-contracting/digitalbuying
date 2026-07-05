# Phase 4a of migrating off wagtailtrans: add a direct page_ptr parent link to
# wagtailcore.Page alongside translatablepage_ptr, copying the (equal) id.
import django.db.models.deletion
from django.db import migrations, models


def copy_page_ptr(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("UPDATE case_studies_casestudieslistingpage SET page_ptr_id = translatablepage_ptr_id")
        cursor.execute("UPDATE case_studies_casestudypage SET page_ptr_id = translatablepage_ptr_id")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("case_studies", "0005_alter_casestudyguidelinessectiontag_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="casestudieslistingpage",
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
            model_name="casestudypage",
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
            model_name="casestudieslistingpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
        migrations.AlterField(
            model_name="casestudypage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to="wagtailcore.page"
            ),
        ),
    ]
