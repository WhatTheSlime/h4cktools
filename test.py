#!/usr/bin/env python3
import asyncio
from h4cktools import *


async def test(s):
	r = await s.get("http://www.google.com")
	return r.url, r.status_code == 200 

if __name__ == "__main__":
	urls = ["https://google.com", "https://facebook.com"]

	s = HTTPSession(workers=1)
	# br.set_proxy("http://127.0.0.1:8080")

	print(s.goto("https://italydeco.fr"))
	print(s.goin("lol"))
	print(s.goin("test"))
	s.prev()
	print(s.goin("lol"))
	print(s.goin("/test"))
	print(s.goout())

