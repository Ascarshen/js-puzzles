import math

def multiplicative_order(a, M):
    """Return the smallest positive integer k such that a^k ≡ 1 (mod M),
    or None if a and M are not coprime."""
    if math.gcd(a, M) != 1:
        return None
    k = 1
    current = a % M
    while current != 1:
        current = (current * a) % M
        k += 1
    return k

# Set the target period L=9.
desired_period = 9
ideal_moduli = []

# Iterate over multiples of 81 within the range [81, 10000)
for M in range(2,100000):
    order = multiplicative_order(10, M)
    # Check if order is defined and divides the desired period
    if order is not None and (desired_period % order == 0):

        ideal_moduli.append((M, order))

print("Ideal moduli (M, order):", ideal_moduli)
