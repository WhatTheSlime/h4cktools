def parse_headers(raw: str) -> dict:
    """
    """
    headers = {}
    lines = list(
        filter(None, [line.replace("\t", "") for line in raw.split("\n")])
    )

    for line in lines:
        try:
            name, value = line.split(":", 1)
            if name != "Host":
                headers[name] = value.strip()
        except ValueError:
            pass
    return headers

def parse_postdata(raw: str) -> dict:
    """
    """
    data = {}
    params = raw.split("&")

    for param in params:
        try:
            name, value = param.split("=")
            data[name] = value
        except ValueError:
            pass

    return data