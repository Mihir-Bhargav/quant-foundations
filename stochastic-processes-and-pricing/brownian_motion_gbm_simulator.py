import numpy as np
import matplotlib.pyplot as plt

class gbm_simulator():
    def __init__(self, N, s0, mu, sigma, T):
        self.N = N           # Number of time steps
        self.s0 = s0
        self.mu = mu
        self.sigma = sigma
        self.dt = T / N
        self.t = np.linspace(0, T, N+1)

    def generate_prices(self, num_simulations=100):
        """
        Generates multiple paths. 
        Returns a 2D array of shape (num_simulations, N + 1)
        """
        # Generate random shocks for all simulations at once
        # Shape: (num_simulations, N)
        dW = np.random.normal(0, np.sqrt(self.dt), (num_simulations, self.N))
        W = np.cumsum(dW, axis=1) 
        
        # Add a column of zeros at the beginning so that W starts at index 0 correctly
        W = np.hstack([np.zeros((num_simulations, 1)), W])

        # Standard GBM formula: S = S0 * exp((mu - 0.5*sigma^2)*t + sigma * W)
        # This applies the calculation across all paths simultaneously
        S = self.s0 * np.exp((self.mu - 0.5 * self.sigma**2) * self.t + 
                               self.sigma * W)
        return S

    def get_most_likely_prices(self):
        # The 'mode' of the distribution: paths follow this if variance is zero
        return self.s0 * np.exp((self.mu - 1.5 * self.sigma**2) * self.t)

    def plot_all_gbms_paths(self, y):
        # 'y' is now a 2D array of shape (num_simulations, N+1)
        plt.figure(figsize=(10,6))
        for i in range(len(y)):
            # Plot each path as its own line
            plt.plot(self.t, y[i], color='b', alpha=0.3) # added alpha for visibility
            
        # Add title and labels
        plt.title('GBM Price Paths')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.grid(True, alpha=0.3)

# --- Execution Block ---
sim = gbm_simulator(N=100, s0=100, mu=0.5, sigma=0.2, T=1.0)

# Now generates 100 distinct paths
prices = sim.generate_prices(num_simulations=100)

# Calculate the average price at each point in time across all simulations
# Note: Since 'prices' is a 2D array, we take the mean along axis 0 (across all simulations)
expected_average_price = np.mean(prices, axis=0)

# Keep your original print statements
print(f"GBM Price (First Path Sample): {prices[0]}") # Showing first path for clarity in logs
print(f"Average Path: {expected_average_price}")

# New print statement for the single most likely final price
most_likely_path = sim.get_most_likely_prices()
print(f"\nMost likely price at terminal time T: {most_likely_path[-1]:.4f}")

sim.plot_all_gbms_paths(prices)
plt.show()
