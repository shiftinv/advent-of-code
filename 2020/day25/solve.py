def mod_discrete_log(base, res, mod):
    # could've probably used Pohlig-Hellman since 20201227 is prime, but bruteforcing the exponent works just as well for smaller numbers
    exp = 0
    value = 1
    while value != res:
        exp += 1
        value = (value * base) % mod
    return exp


with open('input.txt', 'r') as f:
    pubkeys = list(map(int, f.read().splitlines()))

loop0 = mod_discrete_log(7, pubkeys[0], 20201227)
print(pow(pubkeys[1], loop0, 20201227))
