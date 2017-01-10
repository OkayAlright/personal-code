"""
email_verify.py
by Logan Davis

A naive email and url verifier.

I say naive because it is simple
regex matching to common characters in
urls and email addressed that determines
validity.

9/11/16 | Python 3.5 | Editor: Emacs 22
"""
import re

def naive_email_check(emailAddr):
    """
    Returns true if emailAddr is a valid address format.
    Otherwise it returns false.
    """
    if re.fullmatch("^[0-9a-zA-Z\_\-\.]*@[0-9a-zA-Z\_\-\.]*\.[a-zA-Z]*$",emailAddr):
        return True
    else:
        return False

def naive_url_check(urlAddr):
    """
    Returns true if urlAddr is a valid format
    Otherwise false is returned.
    """
    if re.fullmatch("^(|www.)[0-9a-zA-Z\_\-\.]*\.[a-zA-Z]*$", urlAddr):
        return True
    else:
        return False
print(naive_url_check("googlecom"))
