def to_base3(n):
    if n ==0:
        return "0"
    
    base3 = ""
    while n > 0:
        base = str(n%3) + base3
        n //= 3
        
    return base3
