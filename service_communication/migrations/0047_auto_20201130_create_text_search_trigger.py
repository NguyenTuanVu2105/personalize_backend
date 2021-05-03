from django.db import migrations

from HUB.models.random_id_model import RandomIDModel
from service_communication.models import RejectedRequest


def random_id(apps, schema_editor):
    RandomIDModel.init_random_seq(RejectedRequest)

class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('service_communication', '0046_auto_20201130_0633'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION rejected_request_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.object_id::text)), 'A') || setweight(to_tsvector(coalesce(new.detail::text)), 'A') || setweight(to_tsvector(coalesce(new.note::text)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER rejected_request_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "service_communication_rejected_request" FOR EACH ROW EXECUTE PROCEDURE rejected_request_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "service_communication_rejected_request" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER rejected_request_tsv_metadata_search_update ON service_communication_log;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration),
        migrations.RunPython(random_id)
    ]
