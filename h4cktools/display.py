def cat(obj):
    if isinstance(obj, list):
        print("\r\n".join(obj))
    elif isinstance(obj, dict):
        print("\r\n".join(f"{k}: {v}" for k, v in obj.items())
    else:
    	print(str(obj))