from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0040_create_text_search_trigger_ transaction'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION transaction_tsv_metadata_search_trigger() RETURNS trigger AS $$
        declare 
            user_email text;
        begin
            select "user".email into user_email from "billing_transaction" join "billing_general_payment_method" on "billing_transaction".payment_method_id = "billing_general_payment_method".id join "user_settings" on "billing_general_payment_method".user_setting_id = "user_settings".id join "user" on user_settings.user_id = "user".id where "billing_transaction".id = new.id;
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.object_id::text)), 'A') || setweight(to_tsvector(coalesce(user_email)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_transaction" set ID = ID;
    '''

    operations = [
        migrations.RunSQL(migration)
    ]
