#!/usr/bin/env python3
import asyncio
from h4cktools import *

async def main():
	urls = ["https://google.com", "https://facebook.com"]
	br = Browser()
	await br.goto("https://google.com")
	print(extract_versions(br.page.text))

if __name__ == "__main__":
	asyncio.run(main())
	