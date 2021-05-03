from django.http import JsonResponse


class BaseMixin(object):
    error_messages = {}

    def json_error(self, field, code, status=400):
        default_errors = self.error_messages[field]
        errors = {}
        errors.update({"code": code, "message": default_errors[code]})
        return JsonResponse(errors, safe=False, status=status)

    def request_is_valid(self, request, *args):
        request_data = request.data
        for item in args:
            if item not in request_data:
                return False
        return True

    def validator_error(self, request, *args):
        request_data = request.data
        validator = {}
        for item in args:
            if item not in request_data:
                print(item)
                validator.update({item: 'This field is required'})
        response = {
            "success": False,
            "messages": validator
        }
        return JsonResponse(response)
