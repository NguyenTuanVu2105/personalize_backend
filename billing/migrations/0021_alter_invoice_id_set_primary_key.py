from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0020_update_text_search_trigger_20200214_1045'),
    ]

    migration = '''
        alter table billing_invoice add constraint billing_invoice_pk primary key (id);
    '''
    operations = [
        migrations.RunSQL(migration),
    ]
