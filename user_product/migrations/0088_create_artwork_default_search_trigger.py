from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('user_product', '0087_merge_20200925_0813'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION artwork_default_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.name,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER artwork_default_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "artwork_default" FOR EACH ROW EXECUTE PROCEDURE artwork_default_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "artwork_default" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER artwork_default_tsv_metadata_search_update ON artwork_default;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
