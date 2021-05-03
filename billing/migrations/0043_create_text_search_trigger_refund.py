from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0042_auto_20201210_0901'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION refund_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
               new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.object_id::text)), 'A') || setweight(to_tsvector(coalesce(new.invoice_id::text)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER refund_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "billing_refund" FOR EACH ROW EXECUTE PROCEDURE refund_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_refund" set ID = ID;
    '''

    operations = [
        migrations.RunSQL(migration)
    ]
