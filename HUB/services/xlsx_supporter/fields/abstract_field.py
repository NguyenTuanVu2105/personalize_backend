class AbstractField:
    def __init__(self, title='header', plain_text=False, header_style=None, column_width=None, data_style=None,
                 unit_measurement=None):
        self.title = title
        self.header_style = header_style or {}
        self.column_width = column_width or 20
        self.data_style = data_style or {}
        self.unit_measurement = unit_measurement
        self.plain_text = plain_text

    def to_representation(self, instance):
        raise NotImplementedError
