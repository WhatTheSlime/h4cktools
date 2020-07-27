#!/usr/bin/env python3
import asyncio
from h4cktools.browser import Browser

async def main():
	urls = ["https://google.com", "https://facebook.com"]
	br = Browser()
	await br.goto("https://tryenglishapp.com/")
	print(br.page.images())

if __name__ == "__main__":
	asyncio.run(main())
	