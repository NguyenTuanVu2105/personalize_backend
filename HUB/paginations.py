from rest_framework import pagination


class EnhancedPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 10
    max_page_size = 50

    def __init__(self):
        super().__init__()
        self.queryset = None
        self.options = None

    @staticmethod
    def _get_new_pure_queryset(queryset, pure_fields):
        """
        Pagination's queryset contains extra filters (limit, offset) which prevent some options to have global aggregate attributes (Sum, Count)
        -> this function help to prune all field filters in queryset that are not included in pure_fields
        """
        new_queryset = queryset.filter()
        for child_field in new_queryset.query.where.children[:]:
            if not hasattr(child_field, "lhs"):
                continue
            field_name = child_field.lhs.target.name
            if field_name not in pure_fields:
                new_queryset.query.where.children.remove(child_field)
        return new_queryset
