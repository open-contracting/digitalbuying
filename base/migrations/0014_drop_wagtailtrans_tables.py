# Final step of migrating off wagtailtrans: drop its now-unused tables. Uses
# IF EXISTS so it is a no-op on fresh databases (where wagtailtrans was never
# installed). No remaining table references these, so dropping is safe.
from django.db import migrations

TABLES = [
    "wagtailtrans_sitelanguages_other_languages",
    "wagtailtrans_sitelanguages",
    "wagtailtrans_translatablesiterootpage",
    "wagtailtrans_translatablepage",
    "wagtailtrans_language",
]


def drop_tables(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        for table in TABLES:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    # Remove orphaned migration history records for the uninstalled app.
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app = 'wagtailtrans'")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("base", "0013_drop_translatablepage_ptr"),
    ]

    operations = [
        migrations.RunPython(drop_tables, migrations.RunPython.noop),
    ]
