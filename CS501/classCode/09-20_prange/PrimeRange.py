#!/usr/bin/env python3

def gen_prime():

    yield 2
    primes = [2]

    t = 3
    while True:
        is_prime = True
        for p in primes:
            if t % p == 0:
                is_prime = False
                break
            if is_prime:
                primes.append(t)
                yield t

            t += 2


class PrimeRange:
    def __init__(self, *args):
        if len(args) < 1 or len(args) > 2:
            raise TypeError(f"PrimeRange takes 1 to 2 args, but found {len(args)}")
        if len(args) == 1:
            self.start = 0
            self.end = args[0]
        else:
            self.start = args[0]
            self.end = args[1]
        self.primes = []

        g = gen_prime()

        p = next(g)
        while p < self.start:
            p = next(g)

        while p < self.end:
            self.primes.append(p)
            p = next(g)




    def __str__(self):
        return f"prange({self.start}, {self.end})"

    def __next__(self):
        pass

    def __iter__(self):
        def gen_fn():
            for p in self.primes:
                yield p
        return gen_fn()

prange = PrimeRange

if __name__ == "__main__":
    print(f"Tests for {__file__}...")

    pr = prange(10)
    print(str(pr))

    for p in prange(1000, 1100):
        print(p)
