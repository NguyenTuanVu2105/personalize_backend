from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0010_auto_20200114_1518'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION invoice_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_invoice" set ID = ID;
    '''

    operations = [
        migrations.RunSQL(migration)
    ]
