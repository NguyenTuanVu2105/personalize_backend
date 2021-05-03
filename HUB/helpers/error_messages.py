def to_standard_error_messages(var_name_tuples):
    return dict(map(lambda var_name: (var_name[0], to_standard_error_message_by_name(var_name[1])), var_name_tuples))


def to_standard_error_message_by_name(name):
    return {
        'max_length': f'{name} is too long',
        'invalid': f'{name} is invalid'
    }
