from django.db import migrations

from HUB.models.random_id_model import RandomIDModel
from service_communication.models import IncomingWebhook


def random_id(apps, schema_editor):
    RandomIDModel.init_random_seq(IncomingWebhook)


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('service_communication', '0048_auto_20201130_1018'),
    ]
    migration = '''
        CREATE OR REPLACE FUNCTION incoming_webhook_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.object_id::text)), 'A') || setweight(to_tsvector(coalesce(new.body_data::text)), 'A') || setweight(to_tsvector(coalesce(new.process_description::text)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER incoming_webhook_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "service_communication_incoming_webhook" FOR EACH ROW EXECUTE PROCEDURE incoming_webhook_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "service_communication_incoming_webhook" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER incoming_webhook_tsv_metadata_search_update ON service_communication;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration),
        migrations.RunPython(random_id)
    ]
