#!/usr/bin/env python3
import asyncio
from h4cktools import *

async def main():
	urls = ["https://google.com", "https://facebook.com"]
	br = Browser()
	br.set_proxy("http://127.0.0.1:8080")

	await br.goto("https://admin.onlinecreditpolicy.com")
	print(br.page)
	print(br.page.paths)

	await br.goto(br.page.paths[0])
	print(br.page, br.page.paths)

if __name__ == "__main__":
	asyncio.run(main())
	