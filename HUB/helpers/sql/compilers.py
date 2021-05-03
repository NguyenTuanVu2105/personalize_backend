from django.db.models.sql.compiler import SQLCompiler


class NullsAreSmallestSQLCompiler(SQLCompiler):
    def get_order_by(self):
        result = super().get_order_by()
        if result and self.connection.vendor == 'postgresql':
            return [(expr, (sql + (' NULLS LAST' if expr.descending else ' NULLS FIRST'), params, is_ref))
                    for (expr, (sql, params, is_ref)) in result]
        return result
