from django.db import connections
from django.db.models.sql.query import Query

from .compilers import NullsAreSmallestSQLCompiler


class NullsAreSmallestQuery(Query):
    """
    Query that uses custom compiler,
    to utilize PostgreSQL feature of setting position of NULL records
    """

    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]

        # defining that class elsewhere results in import errors

        return NullsAreSmallestSQLCompiler(self, connection, using)
