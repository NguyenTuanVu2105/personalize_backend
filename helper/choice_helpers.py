def find_verbose_type_from_choices(choices: object, target_type: object) -> object:
    for choice in choices:
        type, verbose_type = choice
        if type == target_type:
            return verbose_type
