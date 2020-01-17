import argparse
import os

DEFAULT_HEADERS = [
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) snap "
    "Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding: gzip, deflate",
]

def args_parser():
    """Parse user options for command line utilisation
    """
    # Description
    parser = argparse.ArgumentParser()

    # Session Arguments
    # define target to scan
    parser.add_argument(
        "url", help="target URL (e.g. https://example.com:8080/')"
    )

    # Set custom headers
    parser.add_argument(
        "-H",
        "--headers",
        help="Replace default headers.",
        default=DEFAULT_HEADERS,
        metavar="NAME:VALUE",
        nargs="+",
    )

    # Add custom headers
    parser.add_argument(
        "-aH",
        "--add-headers",
        help="Add header to actual headers (Useful to set cookies with default headers for exemple).",
        default=None,
        metavar="NAME:VALUE",
        nargs="+",
    )

    # allow to check ssl certificate check
    parser.add_argument(
        "--ssl-check",
        help="unauthorize invalid servers certificates",
        action="store_true",
        default=False,
    )

    # Set a proxy
    parser.add_argument(
        "-x",
        "--proxy",
        help="<[protocol://][user:password@]proxyhost[:port]> "
        "use the specified HTTP proxy. If the port number is not specified, "
        "it is assumed at port 8080.",
        default=None,
        metavar="",
    )

    # Set timeout beetween requests
    parser.add_argument(
        "-t",
        "--timeout",
        help="define timeout beetween requests in seconds.",
        default=0,
        metavar="SECONDS",
    )

    parser.add_argument(
        "-w",
        "--workers",
        help="define number of workers for http requests parallelization",
        type=int,
        metavar="NB_WORKERS",
        default=1,
    )

    # Others Arguments

    # Verbose mode
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        help="increase output verbosity",
        default=False,
    )

    # Outputfile
    parser.add_argument(
        "-o",
        "--output",
        help="results folder path",
        type=str,
        default=os.path.abspath("."),
        metavar="RESULTSFOLDERPATH",
    )

    return parser