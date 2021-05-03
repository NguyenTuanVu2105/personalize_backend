from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('shop', '0015_auto_20200219_0736'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION shop_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.name,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER shop_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "shop" FOR EACH ROW EXECUTE PROCEDURE shop_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "shop" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER shop_tsv_metadata_search_update ON shop;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
