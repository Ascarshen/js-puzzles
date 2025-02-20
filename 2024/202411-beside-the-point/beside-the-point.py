from sympy import Rational, atan, integrate, pi, symbols

x, y = symbols('x y')

horizontal_dists = [x, 1 - x]
radii_squared = [d**2 + y**2 for d in horizontal_dists]
angles_to_center = [atan(y / d) for d in horizontal_dists]
sector_slices = [(r_sq * angle - d * y) / 2 for d, r_sq, angle in zip(horizontal_dists, radii_squared, angles_to_center)]
quarter_circle_areas = [(pi * r_sq) / 4 for r_sq in radii_squared]
p_event_given_xy = sum(quarter_circle_areas) - 2 * sum(sector_slices)
prob_A = 8 * integrate(p_event_given_xy, (y, 0, x), (x, 0, Rational(1, 2)))

print(f"Probability P(A) = {prob_A} \n       ≈ {prob_A.evalf():.10f}")
