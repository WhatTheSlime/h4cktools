def to_str(obj):
    if isinstance(obj, list):
        return "\r\n".join(obj)
    if isinstance(obj, dict):
        return "\r\n".join([f"{k}: {v}" for k, v in obj.items()])
    return obj