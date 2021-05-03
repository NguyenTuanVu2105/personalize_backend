from HUB.services.xlsx_supporter.xlsx_workbook_writer import WorkbookWriter


class ModelWorkbook:

    def __init__(self, name):
        self.workbook_writer = WorkbookWriter(name, create_worksheet=False)
        self.worksheets = []

    def append_worksheet(self, worksheet):
        self.worksheets.append(worksheet)

    def get_workbook(self):
        for worksheet in self.worksheets:
            self.workbook_writer.new_worksheet(worksheet.Meta.name)
            self.write_worksheet(worksheet)
        return self.workbook_writer.get_response()

    def write_worksheet(self, worksheet):
        self.workbook_writer.set_default_cell_format(worksheet.cell_format)
        self.workbook_writer.set_heading_format(worksheet.heading_format)
        self.workbook_writer.write_headers(worksheet.get_headers())
        all_fields = worksheet.Meta.fields
        for instance in worksheet.queryset:
            for field in all_fields:
                content, plain_text, cell_format = worksheet.get_content(instance, field)
                self.workbook_writer.write_cell(content, plain_text=plain_text, cell_format_attr=cell_format)
            self.workbook_writer.new_row()
