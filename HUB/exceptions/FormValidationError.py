class FormValidationError(Exception):
    def __init__(self, field=None, code=None, errors=None):
        if errors is not None:
            self.errors = errors
            self.field = next(iter(errors))
            self.code = errors[self.field][0]['code']
        else:
            self.field = field
            self.code = code
