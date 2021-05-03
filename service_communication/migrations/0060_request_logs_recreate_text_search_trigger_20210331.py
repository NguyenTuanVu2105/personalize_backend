from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('service_communication', '0059_auto_20210324_1039'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION webhook_job_log_tsv_metadata_search_trigger() RETURNS trigger AS
        $$
        begin
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text, 'T')), 'A') ||
                                       setweight(to_tsvector(coalesce(new.object_id::text, 'T')), 'A') ||
                                       setweight(to_tsvector(coalesce(new.webhook_job_id::text, 'T')), 'A') ||
                                       setweight(to_tsvector(coalesce(new.payload::text, 'T')), 'A');
            return new;
        end
        $$ LANGUAGE plpgsql;
        
        DROP TRIGGER IF EXISTS webhook_job_log_tsv_metadata_search_update ON public.service_communication_log;
        CREATE TRIGGER webhook_job_log_tsv_metadata_search_update
            BEFORE INSERT OR UPDATE
            ON "service_communication_log"
            FOR EACH ROW
        EXECUTE PROCEDURE webhook_job_log_tsv_metadata_search_trigger();
        
        -- Force triggers to run and populate the text_search column.
        UPDATE "service_communication_log"
        set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER webhook_job_log_tsv_metadata_search_update ON service_communication_log;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
