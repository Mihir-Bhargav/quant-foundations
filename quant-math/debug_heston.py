import numpy as np
from production_system.strategies.heston_hmm.heston.characteristic_fn import heston_cf
from production_system.strategies.heston_hmm.heston.carr_madan import CarrMadanPricer

# Parameters that might cause issues
S, K = 24000, 24000
T = 1.0
r, q = 0.065, 0.012
kappa, theta, sigma, rho, v0 = 2.0, 0.04, 0.25, -0.7, 0.04

u = np.arange(4096) * 0.25
phi = heston_cf(u, S, K, T, r, q, kappa, theta, sigma, rho, v0)
print(f"CF max magnitude: {np.max(np.abs(phi))}")
print(f"CF has NaNs: {np.any(np.isnan(phi))}")

pricer = CarrMadanPricer()
try:
    surface = pricer.price_surface(S, T, r, q, kappa, theta, sigma, rho, v0)
    print(f"Surface ATM IV: {surface.atm_iv(S)}")
except Exception as e:
    print(f"Pricing failed: {e}")
