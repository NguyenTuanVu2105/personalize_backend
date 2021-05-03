def method_permission_required(classes):
    def decorator(function):
        def decorated_function(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return function(self, *args, **kwargs)

        return decorated_function

    return decorator
