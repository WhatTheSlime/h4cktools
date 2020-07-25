#!/usr/bin/env python3
import asyncio
from h4cktools.browser import Browser

async def main():
	urls = ["https://google.com", "https://facebook.com"]
	br = Browser()
	rps = await br.gets(urls)
	print(rs)

if __name__ == "__main__":
	asyncio.run(main())