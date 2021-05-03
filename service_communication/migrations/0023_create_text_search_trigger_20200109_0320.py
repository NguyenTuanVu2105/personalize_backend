from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('service_communication', '0022_auto_20200109_0319'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION webhook_job_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.object_id::text)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER webhook_job_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "service_communication_webhookjob" FOR EACH ROW EXECUTE PROCEDURE webhook_job_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "service_communication_webhookjob" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER webhook_job_tsv_metadata_search_update ON service_communication_webhookjob;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
