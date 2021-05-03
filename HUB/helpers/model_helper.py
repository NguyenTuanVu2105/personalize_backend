def update_object(obj, update_data, allowed_attributes):
    is_updated = False
    for key in update_data:
        if key in allowed_attributes:
            setattr(obj, key, update_data[key])
            is_updated = True
    return is_updated
