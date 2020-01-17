#!/usr/bin/env python3

import asyncio
import os
import subprocess
import yaml

from rqhelper.display import init_logger, display_progress, clear_line
from rqhelper.scopedsession import ScopedSession
from rqhelper.parser import remove_domain, is_local_url, headers_list_to_dict
from rqhelper.args import args_parser


async def dirlist(session, args):
    """Load wordlist and try each words as url

    Args:
        session (rqhelper.ScopedSession): session to make HTTP requests
        args (argparse.Namespace): program parameters
    """
    #: list of words to try on target
    wordlist = []

    # Try first connexion to the target by requesting "/" and setting up session 
    # object
    await session.set_index_response()
    logger.info(
        f"Target is: {session.scope}, "
        f"code: {session.index_response.status_code}"
    )

    # Try to load the wordlist
    logger.info(f"Loading {args.wordlist}...")
    try:
        with open(
            args.wordlist, "r", encoding="utf8", errors='ignore'
        ) as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                if word not in wordlist:
                    wordlist.append(args.preffix + word + args.suffix)
        logger.notice("Wordlist loaded.")
    except IOError as e:
        logger.exception(e)

    # Creating asynchronus requests tasks
    futures = [
        asyncio.create_task(
            session.get(url, allow_redirects=False)
        ) for url in wordlist
    ]

    # Launching asynchronus requests
    for i, future in enumerate(asyncio.as_completed(futures)):
        #: rqhelper.WrappedResponse object
        response = await future
        # Display progress bar
        display_progress(i+1, len(futures))
        
        if response.is_ok():
            clear_line()
            logger.success(f"{response.status_code} {response.url}")
            inputs = response.tags("form")
            for tag in inputs:
                logger.success(f"- form : {tag.attrs}")
        elif response.is_present():
            clear_line()
            logger.notice(f"{response.status_code} {response.url}")
        
    # Removing progress bar
    clear_line()

if __name__ == "__main__":
    """This program is a tool to list directories on a web server.
    """
    #: argparse.ArgumentParser object
    parser = args_parser()
    parser.add_argument("wordlist", help="Wordlist path")
    parser.add_argument(
        "-p,", 
        "--preffix", 
        help="Preffix to add to words",  
        metavar="Preffix",
        default=""
    )
    parser.add_argument(
        "-s,", 
        "--suffix", 
        help="Suffix to add to words",  
        metavar="Preffix",
        default=""
    )
    #: argparse.NameSpace object
    args = parser.parse_args()
    #: logging.Logger object
    logger = init_logger(__module__, args.output, args.verbosity)
    #: rqhelper.ScopedSession object
    session = ScopedSession(args.url, workers=args.workers)
    session.set_headers(args)

    # Start dirlisting
    asyncio.run(dirlist(session, args))
    # End dirlisting
    logger.info("Program ended")


