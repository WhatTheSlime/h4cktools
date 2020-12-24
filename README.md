# H4ckTools

## Purpose
h4cktools is a library containing usefull helpers for penetration testing, security challenges and CTF.
It include all python library that can be useful, implements several new functions ond objects and add shorcuts for functions and payloads.

h4cktools was developped by a random pentester who loves python language <3

The project is compatible with Windows and Unix based systems.

It is Web Pentest Oriented, it is not inclding pwntools and it does not have not the same purpose.

## Disclaimer
This project is in not intended to be used for illegal purpose and h4cktools developers are in no way responsible for its use.

## Summary

## Install
```bash
$ pip3 install git+https://github.com/WhatTheSlime/h4cktools.git
```

## How to use
h4cktools library has been developped for be used in a python prompt like [IPython](https://ipython.org/)

To use it just open a python prompt and import all components of the library:
```python
>>> from h4cktools import *
```
Of course it can also be used in scripts but it is not recommended to use h4cktools in long-term project.

## HTTPSession
HTTP library aims to execute HTTP requests and parse its content easily. It is override requests library to be use quicker and addapt it to pentesting

### Initialization:
```python
>>> s = HTTPSession()
```

### Navigate into a host
#### Goto

The main feature of HTTPSession is to send get requests by using *goto* method:
```python
>>> s.goto("https://www.google.com")
<[200] http://www.google.com/>
```

HTTP Session works as a browser, when you reach an url the session store the response in *page* attributes:
```python
>>> s.goto("https://www.google.com")
<[200] http://www.google.com/>
>>> s.page
<[200] http://www.google.com/>
```
Page attributes is a requests.Response wrapper that add parsing attributes and methods. (See Response parsing section)

If url contains scheme and domain name, *host* attribute will be set .
When the *host* is set, you can navigate into the host using local path:
```python
>>> s.goto("/webph")
<[200] https://www.google.com/webhp>

>>> s.goto("webph")
<[200] https://www.google.com/webhp>
```

Scope can also be initialize at HTTPSession declaration or set after without doing any requests:
```python
>>> s = HTTPSession("https://www.google.com")
>>> s.host
'https://www.google.com'
>>> s.host = "https://facebook.com"
>>> s.host
'https://facebook.com'
```

Note that redirection following is disable by default. When a response must redirect, you can use *follow* method to go on:
```python
>>> s.goto("https://google.com")
<[301] https://google.com/>

>>> s.follow()
<[200] https://www.google.com/>
```

#### Web tree navigation

*goin* and *goout* methods allow you to navigate in web tree, similar to cd <Local_Path> and cd ../ unix commands:
```python
>>> s.goto("https://google.com")
<[200] https://www.google.com/>

>>> s.goto("search")
<[302] https://www.google.com/search>

>>> s.follow()
<[200] https://www.google.com/webhp>

>>> s.goout()
<[200] https://www.google.com/>
```

To check your current path, simply check the *page* attribute or, if you only want the path, use the page.path attribute:
```python
>>> s.goto("https://www.google.com")
<[200] https://www.google.com/>

>>> s.page
<[200] https://www.google.com/>
>>> s.page.path
'/'
```

#### Historic

HTTPSession keep visited pages as a browser, historic is cached in hist attribute:
```python
>>> s.goto("https://google.com")
<[301] https://google.com/>
>>> s.follow()                                                                                      
<[200] https://www.google.com/>
>>> s.hist                                                    
[<[301] https://google.com/>, <[200] https://www.google.com/>]
```

You can also reach previous and next page using *prev* and *next* methods:
```python
>>> s.goto("https://www.google.com")
<[200] https://www.google.com/>
>>> s.goto("https://www.google.com/webhp")
<[200] https://www.google.com/webhp>
>>> s.prev()
<[200] https://www.google.com/>
>>> s.next()
<[200] https://www.google.com/webhp>
```

### Asynchronous Requests
With this library, it is not possible to call *get* or *post* method like requests library.
In fact, if you try to do it, it will not return send a request and not return a response:
```python
>>> s.get("https://www.google.com")
<Future pending cb=...
```
Return of get method is a prepared request as asyncio Future object.

To send this request you need to call await the task:
```python
>>> await s.get("https://www.google.com")
[<[200] https://www.google.com/>]
```

Or use the *run* method:
```python
>>> s.run(s.get("https://www.google.com"))
[<[200] https://www.google.com/>]
```

Futures object allow you to send requests concurrently:
```python
>>> rqs = [s.get(f"https://www.google.com/{i}") for i in range(1, 5)]
>>> s.run(*rqs)
[<[404] https://google.com/4>,
 <[404] https://google.com/0>,
 <[404] https://google.com/1>,
 <[404] https://google.com/2>,
 <[404] https://google.com/3>]
```

If you want to use specific actions on each response, it is also possible by declaring functions with async syntax
```python
TODO
```

You can define worker number at HTTPSession initialization or after:
```python
>>> s = HTTPSession(workers=5)
>>> s.workers = 5
```

Note that doing requests in this way will note populate the history and set current page of th HTTPSession.

### Responses Parsing

## Encoder

## Display
Display library include following functions:
- cat: display all python basic object in form of a string

### cat
Example:
```python
# Lists
>>> cat()
>>> cat()

# Dicts
>>> d = {1: "first", 2: "second"}
1: first
2: second
```

## References
