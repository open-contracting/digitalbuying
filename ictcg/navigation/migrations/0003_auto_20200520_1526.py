# Generated by Django 3.0.5 on 2020-05-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0002_auto_20200504_0835_squashed_0006_footermenu_sponsors_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmenu',
            name='logo_description',
            field=models.CharField(blank=True, help_text='Alt tag description for logo', max_length=240, null=True),
        ),
        migrations.AddField(
            model_name='sponsoritem',
            name='logo_description',
            field=models.CharField(blank=True, help_text='Alt tag description for sponsor logo', max_length=240, null=True),
        ),
    ]
