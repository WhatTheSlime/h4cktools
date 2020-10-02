#!/usr/bin/env python3
import asyncio
import time
from h4cktools.http.asyncsession import AsyncSession
from h4cktools.http.httpsession import HTTPSession


if __name__ == "__main__":
	s = HTTPSession()
	s.proxies["https"] = "http://127.0.0.1:8080"
	s.verify = False
	print(s.thread_pool._max_workers)
	
	rqs = s.get(f"https://italydeco.fr/", redirects=True)

	rps = s.run(rqs)
	
	rps.soup()

	print(rps.tags("a"))