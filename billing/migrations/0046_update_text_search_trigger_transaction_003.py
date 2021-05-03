from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('billing', '0045_update_text_serach_trigger_transaction_20122020_1234'),
    ]

    migration = '''
        DROP TRIGGER transaction_tsv_metadata_search_update ON billing_transaction;
        CREATE OR REPLACE FUNCTION transaction_tsv_metadata_search_trigger() RETURNS trigger AS $$
        declare 
            user_email text;
        begin
            select "user".email into user_email from "billing_general_payment_method"  join "user_settings" on "billing_general_payment_method".user_setting_id = "user_settings".id join "user" on user_settings.user_id = "user".id where "billing_general_payment_method".id = new.payment_method_id;
            new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.object_id::text)), 'A') || setweight(to_tsvector(coalesce(user_email)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER transaction_tsv_metadata_search_update AFTER INSERT OR UPDATE
        ON "billing_transaction" FOR EACH ROW EXECUTE PROCEDURE transaction_tsv_metadata_search_trigger();
        -- Force triggers to run and populate the text_search column.
        UPDATE "billing_transaction" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER transaction_tsv_metadata_search_update ON billing_transaction;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
