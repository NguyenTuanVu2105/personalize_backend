from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('order', '0016_auto_20191027_1758'),
    ]

    migration = '''
     CREATE OR REPLACE FUNCTION order_tsv_metadata_search_trigger() RETURNS trigger AS $$
        declare 
            customer_info text;
        begin
            SELECT CONCAT(first_name,' ', last_name, ' ', email) into customer_info FROM order_customer_info WHERE id = new.customer_info_id;
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.order_id,'')), 'A') || setweight(to_tsvector(coalesce(new.order_number,'')), 'A') || setweight(to_tsvector(coalesce(customer_info,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        -- Force triggers to run and populate the text_search column.
        UPDATE "order" set ID = ID;
    '''
    operations = [
        migrations.RunSQL(migration)
    ]
