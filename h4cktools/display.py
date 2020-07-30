def cat(obj) -> str:
    """Return string shaped object

    Args:
        obj: Object to string transform

    Returns:
        str: string form of the object
    """
    if isinstance(obj, list):
        return "\r\n".join(obj)

    if isinstance(obj, dict):
        return "\r\n".join(f"{k}: {v}" for k, v in obj.items())
    
    return(str(obj))