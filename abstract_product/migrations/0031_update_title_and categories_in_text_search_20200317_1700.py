from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('abstract_product', '0030_abstractproduct_tsv_metadata_search'),
    ]

    migration = '''
     CREATE OR REPLACE FUNCTION abstract_product_tsv_metadata_search_trigger() RETURNS trigger AS $$
        declare 
            categories text;
        begin
            SELECT string_agg(title, ' , ') into categories FROM abstract_product_category INNER JOIN abstract_product_abstract_category apac on abstract_product_category.id = apac.category_id WHERE product_id = new.id GROUP BY product_id;
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.title,'')), 'A') || setweight(to_tsvector(coalesce(categories,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER abstract_product_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON "abstract_product" FOR EACH ROW EXECUTE PROCEDURE abstract_product_tsv_metadata_search_trigger();

        
        -- Force triggers to run and populate the text_search column.
        UPDATE "abstract_product" set ID = ID;
    '''
    operations = [
        migrations.RunSQL(migration)
    ]
