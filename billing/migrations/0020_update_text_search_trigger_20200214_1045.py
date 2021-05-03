from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0019_auto_20200211_0650'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION invoice_tsv_metadata_search_trigger() RETURNS trigger AS $$
        declare 
            order_ids_joined_str text;
        begin
            SELECT string_agg(DISTINCT "order_pack"."order_id"::text, ' ') INTO order_ids_joined_str FROM "billing_invoice" LEFT OUTER JOIN "billing_invoicepack" ON ("billing_invoice"."id" = "billing_invoicepack"."invoice_id") LEFT OUTER JOIN "order_pack" ON ("billing_invoicepack"."order_pack_id" = "order_pack"."id") WHERE "billing_invoice"."id" = new.id GROUP BY "billing_invoice"."id";
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(order_ids_joined_str,'')), 'B');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_invoice" set ID = ID;
    '''

    operations = [
        migrations.RunSQL(migration)
    ]
