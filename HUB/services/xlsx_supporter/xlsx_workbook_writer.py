import json

from django.http import HttpResponse
from xlsxwriter import Workbook


class WorkbookWriter:
    def __init__(self, filename='workbook', *args, **kwargs):
        self.response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.filename = filename
        self.response['Content-Disposition'] = "attachment; filename={}.xlsx".format(self.filename)
        self.workbook = Workbook(self.response, {'in_memory': True})
        self.default_cell_format = self.workbook.add_format()
        self.heading_format = self.workbook.add_format()
        self.worksheet = None
        self.row = self.col = None
        create_worksheet = kwargs.get('create_worksheet')
        if create_worksheet is None or create_worksheet:
            worksheet_name = kwargs.get('worksheet_name')
            self.new_worksheet(worksheet_name)

    def set_default_cell_format(self, format_attr):
        self.default_cell_format = self.workbook.add_format(format_attr)

    def set_heading_format(self, format_attr):
        self.heading_format = self.workbook.add_format(format_attr)

    def new_worksheet(self, name=None):
        self.worksheet = self.workbook.add_worksheet(name)
        self.row = self.col = 0

    def new_row(self, number=1):
        self.row += number
        self.col = 0

    def ignore_cell(self):
        self.col += 1

    def write_headers(self, headers_kwargs):
        for header_kwargs in headers_kwargs:
            self._write_header(**header_kwargs)
        self.new_row()

    def _write_header(self, title, style=None, column_width=20, unit=None):
        content = f'{title} ({unit})' if unit else title
        self.worksheet.set_column(self.col, self.col, width=column_width)
        self.write_cell(content, plain_text=True, cell_format_attr=style or self.heading_format)

    def write_cell(self, content, plain_text=False, cell_format_attr=None):
        cell_format = cell_format_attr or self.default_cell_format
        if type(content) is dict:
            content = json.dumps(content, ensure_ascii=False)
        elif type(content) is list:
            content = ',\n'.join(content)
        if plain_text and content and type(content) is str and content[0].islower():
            content = content[0].upper() + content[1:]
        self.worksheet.write(self.row, self.col, content, cell_format)
        self.col += 1

    def get_response(self):
        self.workbook.close()
        return self.response
