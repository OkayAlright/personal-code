def isPrime(p,a):
    """
    Will return true if p is prime or a Carmichael number.
    """
    return (a**(p-1))%p == 1
