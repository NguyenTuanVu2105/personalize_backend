from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('user', '0044_auto_20201020_0440'),
    ]

    migration = '''
        CREATE OR REPLACE FUNCTION user_metadata_search_trigger() RETURNS trigger AS $$
        begin
          new.tsv_metadata_search := setweight(to_tsvector(coalesce(new.id::text)), 'A') || setweight(to_tsvector(coalesce(new.email::text)), 'A') || setweight(to_tsvector(coalesce(new.name::text)), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER user_metadata_search_update BEFORE INSERT OR UPDATE
        ON "user" FOR EACH ROW EXECUTE PROCEDURE user_metadata_search_trigger();

        -- Force triggers to run and populate the text_search column.
        UPDATE "user" set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER user_metadata_search_update ON user;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
