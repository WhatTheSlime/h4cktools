def ip_args(parser):
    """Add ip arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    hosts = parser.add_mutually_exclusive_group(required=required)
    hosts.add_argument(
        "-i",
        "--ip", 
        help="Define an ip addresse: <IP> <PORT>",
        metavar=["IP", "PORT"],
        nargs=2,
        type=str,
    )
    hosts.add_argument(
        "-il",
        "--ip-list",
        help="Path to a list of url: <IP>:<PORT> on each line",
        metavar="PATH",
        type=str,
    )

def urls_args(parser, required=True):
    """Add urls arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    urls = parser.add_mutually_exclusive_group(required=required)
    urls.add_argument(
        "-u", 
        "--url", 
        help="Define a url: [scheme]://[host]:[port]",
        metavar="URL",
        type=str,
    )
    urls.add_argument(
        "-ul",
        "--url-list",
        help="Path to a list of url: [scheme]://[host]:[port] on each line",
        metavar="PATH",
        type=str,
    )


def connect_back_args(parser):
    """Add connect back arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    connect_back = parser.add_argument_group("Connect Back")

    # Set server for connect back
    connect_back.add_argument(
        "-cb", 
        "--connect-back",
        help="Define a server for connect back: <IP> <PORT>",
        metavar=["IP", "PORT"],
        nargs=2,
    )

def session_args(parser):
    """Add session arguments to parser

    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    session = parser.add_argument_group("Session")

    # Set custom headers
    session.add_argument(
        "-H",
        "--headers",
        help="replace default headers.",
        metavar="NAME:VALUE",
        nargs="+",
    )

    # Add custom headers
    session.add_argument(
        "-aH",
        "--add-headers",
        help="add header to actual headers "
        "(Useful to set cookies with default headers for exemple).",
        metavar="NAME:VALUE",
        nargs="+",
    )

    # Set a proxy
    session.add_argument(
        "-x",
        "--proxy",
        help="Use the specified HTTP proxy as "
        "[protocol]://[user]:[password]@[proxyhost]:[port]. "
        "If the port number is not specified, it is assumed at port 8080.",
        metavar="PROXY",
        type=str,
    )

    session.add_argument(
        "-T",
        "--threads",
        help="define number of workers for http requests parallelization",
        type=int,
        metavar="NB_THREADS",
        default=5,
    )

    # Allow to check ssl certificate check
    session.add_argument(
        "--ssl-check",
        help="unauthorize invalid servers certificates.",
        action="store_true",
        default=False,
    )

    # Set timeout beetween requests
    session.add_argument(
        "-d",
        "--delay",
        help="define time delay beetween requests in seconds.",
        metavar="SECONDS",
        default=0,
        type=float,
    )
