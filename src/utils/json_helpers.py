def find_text(json_data, **key_value):
    if isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                if all(item.get(k) == v for k, v in key_value.items()):
                    return item
    return None
