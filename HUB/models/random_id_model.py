from django.db import models, connection

from helper.model_helpers import generate_random_code
from helper.string_helpers import convert_camel_to_underscore


class RandomIDModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, unique=True)

    class Meta:
        abstract = True

    @property
    def model_name(self):
        model_name = self.__class__.__name__
        return convert_camel_to_underscore(model_name)

    @staticmethod
    def init_random_seq(model):
        id = generate_random_code()
        with connection.cursor() as cursor:
            table_name = model._meta.db_table
            sequence_name = f'{table_name}_seq'
            cursor.execute(f"CREATE SEQUENCE IF NOT EXISTS {sequence_name} START 0 minvalue 0 maxvalue 9223372036854775807 increment by 1")
            cursor.execute(f"ALTER SEQUENCE {sequence_name} as bigint maxvalue 9223372036854775807")
            cursor.execute(f"SELECT setval('{sequence_name}', {id})")
            cursor.execute(f"alter table public.{table_name} alter column id set default nextval_rand('{sequence_name}'::regclass)")
            cursor.execute("COMMIT")
