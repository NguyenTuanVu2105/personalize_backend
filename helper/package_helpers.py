def get_package_name(package_name=__name__):
    return package_name.split(".", 1)[0]
