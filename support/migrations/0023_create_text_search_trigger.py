from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('support', '0022_update_customer_send_values'),
    ]

    migration = '''
        CREATE OR REPLACE  FUNCTION support_ticket_tsv_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.subject,'')), 'A') || setweight(to_tsvector(coalesce(new.description,'')), 'B');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER support_ticket_tsv_metadata_search_update BEFORE INSERT OR UPDATE
        ON support_ticket FOR EACH ROW EXECUTE PROCEDURE support_ticket_tsv_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE support_ticket set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER support_ticket_tsv_metadata_search_update ON support_ticket;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
