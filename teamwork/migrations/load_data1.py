from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    fixture = 'data1'

    call_command('loaddata', fixture, app_label='teamwork') 


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0008_auto_20161019_2349'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
