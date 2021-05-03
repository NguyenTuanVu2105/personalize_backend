from django.db.models.query import QuerySet

from HUB.helpers.sql.queries import NullsAreSmallestQuery


class NullsAreSmallestQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)
        self.query = query or NullsAreSmallestQuery(self.model)
