def mdcEstendido(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1

    while True:
        resto = a % b

        if resto == 0:
            return {
                "coef1": x1,
                "coef2": y1,
                "mdc": b
            }
        
        q = a // b
        a = b
        b = resto
        aux1, aux2 = x0, y0
        x0, y0 = x1, y1
        x1, y1 = -q * x0 + aux1, -q * y0 + aux2

def ehPrimo(n):
    if n <= 1: 
        return False
    if n == 2: 
        return True
    if n % 2 == 0: 
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
            
    return True


def proximoPrimo(n):
    n += 1

    if n <= 2:
        return 2
    if n % 2 == 0:
        n += 1
        
    while not ehPrimo(n):
        n += 2
    return n

def exponenciacaoModular(num, expoente, m):
    return pow(num, expoente, m)
