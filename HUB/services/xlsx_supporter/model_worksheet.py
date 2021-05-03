class ModelWorksheet:
    def __init__(self, queryset, cell_format=None, heading_format=None):
        self.queryset = queryset
        self.cell_format = cell_format or {}
        self.heading_format = heading_format or {}

    def get_content(self, instance, field_name):
        field = getattr(self, field_name)
        return field.to_representation(instance), field.plain_text, field.data_style

    def get_headers(self):
        ret_headers = []
        for field_name in self.Meta.fields:
            field = getattr(self, field_name)
            ret_headers.append({
                'title': field.title,
                'column_width': field.column_width,
                'style': field.header_style,
                'unit': field.unit_measurement
            })
        return ret_headers

    class Meta:
        name = 'model'
        fields = []
