# Phase 4b of migrating off wagtailtrans: drop translatablepage_ptr and make
# page_ptr the primary key. CaseStudyGuidelinesSectionTag.content_object is a
# ParentalKey to CaseStudyPage, so its FK must be dropped before the old PK
# column can go, then re-pointed at the new page_ptr_id PK.
import django.db.models.deletion
from django.db import migrations, models

CHILD_TABLE = "case_studies_casestudyguidelinessectiontag"
PARENT_TABLE = "case_studies_casestudypage"


def drop_child_fk(apps, schema_editor):
    with schema_editor.connection.cursor() as c:
        c.execute(
            """SELECT constraint_name FROM information_schema.key_column_usage
               WHERE table_schema = DATABASE() AND table_name = %s
               AND column_name = 'content_object_id' AND referenced_table_name IS NOT NULL""",
            [CHILD_TABLE],
        )
        for (name,) in c.fetchall():
            c.execute(f"ALTER TABLE {CHILD_TABLE} DROP FOREIGN KEY `{name}`")


def add_child_fk(apps, schema_editor):
    with schema_editor.connection.cursor() as c:
        c.execute(
            f"ALTER TABLE {CHILD_TABLE} ADD CONSTRAINT "
            f"case_studies_casestudyguidelinessectiontag_content_object_id_fk "
            f"FOREIGN KEY (content_object_id) REFERENCES {PARENT_TABLE}(page_ptr_id)"
        )


def drop_re_added_fk(apps, schema_editor):
    with schema_editor.connection.cursor() as c:
        c.execute(
            f"ALTER TABLE {CHILD_TABLE} DROP FOREIGN KEY "
            f"case_studies_casestudyguidelinessectiontag_content_object_id_fk"
        )


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("case_studies", "0006_collapse_translatablepage_mti"),
    ]

    operations = [
        migrations.RunPython(drop_child_fk, add_child_fk),
        migrations.RemoveField(
            model_name="casestudieslistingpage",
            name="translatablepage_ptr",
        ),
        migrations.RemoveField(
            model_name="casestudypage",
            name="translatablepage_ptr",
        ),
        migrations.AlterField(
            model_name="casestudieslistingpage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.AlterField(
            model_name="casestudypage",
            name="page_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="wagtailcore.page",
            ),
        ),
        migrations.RunPython(add_child_fk, drop_re_added_fk),
    ]
