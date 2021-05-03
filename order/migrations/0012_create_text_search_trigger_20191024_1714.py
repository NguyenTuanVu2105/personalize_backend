from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('order', '0011_auto_20191024_1712'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION order_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.order_id,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER order_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "order" FOR EACH ROW EXECUTE PROCEDURE order_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "order" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER order_tsv_metadata_search_update ON order;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
