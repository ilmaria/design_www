from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    fixture = 'data2'

    call_command('loaddata', fixture, app_label='teamwork') 


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
