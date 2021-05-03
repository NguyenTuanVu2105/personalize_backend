from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0005_auto_20191024_1732'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION invoice_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER invoice_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "billing_invoice" FOR EACH ROW EXECUTE PROCEDURE invoice_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_invoice" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER invoice_tsv_metadata_search_update ON billing_invoice;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
