from random import randint, choice
from string import ascii_letters, digits


def randnum(length: int) -> str:
    """Generate random number of certain length

    Args:

    Returns:
        int: genreate
    """
    return "".join([str(randint(0, 9)) for i in range(0, length)])


def password(length: int = 20) -> str:
    """Generate strong password

    Args:
        length (int): password length

    Returns:
        str: generated password 
    """
    characters = "".join([ascii_letters, digits, "_-~&!+"])
    return "".join((choice(characters) for i in range(length)))


def phpserialize(obj, null_byte="\0") -> str:
    """Serialize object like serialize function do in php

    Args:
        obj (): Built in type object
    """
    if isinstance(obj, type(None)):
        return "N;"
    if isinstance(obj, int):
        return f"i:{obj};"
    if isinstance(obj, float):
        return f"d:{obj};"
    if isinstance(obj, bool):
        return f"b:{int(obj)};"
    if isinstance(obj, str):
        return f"s:{len(obj)}:\"{obj}\";"
    if isinstance(obj, dict):
        s = "".join(
            [f"{phpserialize(k)}{phpserialize(v)}" for k, v in obj.items()] 
        )
        return s.join([f"a:{len(obj)}:{{", f"}}"])
    if isinstance(obj, (list, tuple, set)):
        s = "".join(
            [f"{phpserialize(i)}{phpserialize(v)}" for i, v in enumerate(obj)]
        )
        return s.join([f"a:{len(obj)}:{{", f"}}"])
    if isinstance(obj, object):
        n = obj.__class__.__name__
        s = f"O:{len(n)}:{n}:{len(vars(obj))}:{{"
        for k, v in vars(obj).items():
            nk = k
            # Attribute is private
            if k.startswith(f"_{n}__"):
                nk = "".join([null_byte, n, null_byte, k[len(f"_{n}__"):]])              
            # Attribute is protected
            elif k.startswith("_"):
                nk = "".join([null_byte, "*", null_byte, k[1:]])

            s += phpserialize(nk)
            s += phpserialize(v)
        s += "}}"
        return s


def javaserialize(obj):
    """
    """
    pass


'''
def iban() -> str:
    """Generate random valid iban number
    TODO
    """
    pass

def visacard() -> int:
    """
    """
    num = 0
    while not verifycard(num):
        num = int("".join(str(randint(0, 9)) for i, _ in enumerate(range(0, 16))))
    return num

def creditcard(length):
    num = [randint(0, 9) for i, _ in enumerate(range(0, length - 1))]
    checksum = sum(num)%10

    print(num, checksum)

    for i, _ in enumerate(num): 
        if nu

    for i, _ in enumerate(num):
        if i%2 == 0:
            num[i] = int(num[i]/2)

    num = num[::-1]

    num += [checksum]

    return int("".join(str(n) for n in num))


def verifycard(number: int) -> int:
    num = str(number).split()
    
    checksum = num[:-1]

    # Drop the last digit
    if len(num) > 0:
        num = num[:-1]
    
    # Reverse the digits
    num = num[::-1]

    # Multiple odd digits by 2
    for i, _ in enumerate(num): 
        if i%2 == 0:
            num[i] *= 2

    # Subtract 9 to numbers over 9
    for i, _ in enumerate(num):
        if num[i] > 9:
            num[i] -= 9

    return sum(num)%10 == checksum
'''