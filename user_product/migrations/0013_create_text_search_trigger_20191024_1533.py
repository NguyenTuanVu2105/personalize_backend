from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('user_product', '0012_auto_20191024_1531'),
    ]

    migration = '''
        CREATE OR REPLACE  FUNCTION user_product_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.title,'')), 'A') || setweight(to_tsvector(coalesce(new.description,'')), 'B');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER user_product_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON user_product FOR EACH ROW EXECUTE PROCEDURE user_product_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE user_product set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER user_product_tsv_metadata_search_update ON user_product;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
