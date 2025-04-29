import math

CYCLIC_NUMBER = 111_111_111
d_values = [1, 3, 4, 6, 7, 8, 9]
N_dict = {d: CYCLIC_NUMBER * (45 - d) for d in d_values}
N_values = list(N_dict.values())
gcd_all = math.gcd(*N_values)

# 计算因子
gcd_factors = set()
for i in range(1, int(gcd_all**0.5) + 1):
    if gcd_all % i == 0:
        gcd_factors.add(i)
        gcd_factors.add(gcd_all // i)
gcd_factors = sorted(gcd_factors)

d_from_N = {N: 45 - (N // CYCLIC_NUMBER) for N in N_values}

print("Excluded d values and their corresponding N_d:")
for N, d in d_from_N.items():
    print(f"Excluded {d}: N_d = {N}")
print(f"\nGCD of all N_d: {gcd_all}")
print(f"Factors of GCD: {gcd_factors}")
