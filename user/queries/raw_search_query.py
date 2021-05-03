from django.contrib.postgres.search import SearchQuery


class RawSearchQuery(SearchQuery):
    """Override to use to_tsquery instead of plainto_tsquery

    Allows formatted search terms for things like prefix matching search.

    This feature is coming in django 2.2 in april 2019 so remove and use that when
    possible.
    """

    def as_sql(self, compiler, connection):
        params = [self.value]
        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = 'to_tsquery({}::regconfig, %s)'.format(config_sql)
            params = config_params + [self.value]
        else:
            template = 'to_tsquery(%s)'
        if self.invert:
            template = '!!({})'.format(template)
        return template, params
