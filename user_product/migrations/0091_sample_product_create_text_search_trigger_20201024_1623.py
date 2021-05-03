from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('user_product', '0090_auto_20201024_0935'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION sample_product_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.title,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER shop_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "sample_product" FOR EACH ROW EXECUTE PROCEDURE sample_product_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "sample_product" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER sample_product_tsv_metadata_search_update ON shop;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
