from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('user_product', '0038_auto_20200114_0616'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION artwork_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.name,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER artwork_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "artwork" FOR EACH ROW EXECUTE PROCEDURE artwork_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "artwork" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER artwork_tsv_metadata_search_update ON artwork;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
