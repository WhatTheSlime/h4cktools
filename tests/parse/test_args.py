import argparse
import os
import sys

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.parse.args import (
    ip_args, urls_args, connect_back_args, session_args, output_args
)

def test_ip_args():
    parser = argparse.ArgumentParser([])
    ip_args(parser)

def test_urls_args():
    parser = argparse.ArgumentParser([])
    urls_args(parser)

def test_connect_back_args():
    parser = argparse.ArgumentParser()
    connect_back_args(parser)

def test_session_args():
    parser = argparse.ArgumentParser([])
    session_args(parser)

def test_output_args():
    parser = argparse.ArgumentParser([])
    output_args(parser)