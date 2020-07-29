#!/usr/bin/env python3
import asyncio
from h4cktools import *


async def test(s):
	r = await s.get("http://www.google.com")
	return r.url, r.status_code == 200 

if __name__ == "__main__":
	urls = ["https://google.com", "https://facebook.com"]

	s = HTTPSession(workers=10)
	# br.set_proxy("http://127.0.0.1:8080")

	string = "heyyyyy sdfsqdqsdf qdfqsdfq"

	test = b64encode(string)
	print(b64encode(string))
	print(str(b64decode(b64encode(string))))

	print(furlencode(string))
	print(urldecode(furlencode(string)))

	print(urlb64encode(string))
	print(urlb64decode(urlb64encode(string)))

