import numpy as np  
import math 
import matplotlib.pyplot as plt

# Bionomial distributions have 4 requirements which can be remembered with BINS
# B = Binary outcomes, I = Independent trials, N = "N" trails, S = Same p per trial 
# Once these are met, we can use the bionomial distribution 

# n = trials, p = prob sucess, q = prob failiure
# Mean (mu) = n x p 
#std.dev = sqrt(n x p (1-p)) = sqrt(npq)

#Rolling a die 4 times; Prob(1 twice?): P(X = x): (n choose x) p^xq^n-x
# (n choose x) describes how many ways there are to get the desired outcome. 
# It is given by this factorial; n!/(n-x)!x! 
# in essence, we find the probability of it happening once from the right term (p^x q^n-x) and multiply by the number of times it can happen (n choose x)
# so in final; (n choose x) p^x q ^n-x 


class binomial_dist(): 
    def __init__(self, n, p, k):  
        self.n = n 
        self.p = p 
        self.k = k 

    def compute_binomial(self): 
        # lets define the (n choose x term as t1) 
        self.t1 = math.factorial(self.n) / (math.factorial(self.n - self.k) * math.factorial(self.k)) 
        # let t2 be the right part of the formula: 
        self.t2 = (self.p) ** self.k * (1-self.p) ** (self.n - self.k) 
        self.px = self.t1 * self.t2 
        print(f" The probability is {100*self.px}%") 
        return self.px

    def compute_mu_std(self): 
        print("..")
        self.mean = self.n * self.p 
        self.std = math.sqrt(self.n * self.p * (1-self.p))
        print(f"Mean: {self.mean} | Standard deviation:{self.std}")
        # we will have to calculate mean and standard deviation for a binomial distribution 
    
    def plot_chart(self): 
        x_values = list(range(self.n + 1))

        # Just recalculatge quickly to avoid that bug
        y_values = []
        for x in x_values:
            t1 = math.factorial(self.n) / (math.factorial(self.n - x) * math.factorial(x))
            t2 = (self.p) ** x * (1 - self.p) ** (self.n - x)
            y_values.append(t1 * t2)
            
        colors = ['red' if x == self.k else "#5496c5" for x in x_values] 
        plt.figure(figsize=(10, 5))
        plt.bar(x_values, y_values, color=colors, width=0.8)
        plt.title(f"Binomial Distribution (n={self.n}, p={self.p}) | Highlighting k={self.k}")
        plt.xlabel("Number of Successes (x)")
        plt.ylabel("Probability P(x)")
        plt.grid(axis='y', alpha=0.3)
        plt.show()





test = binomial_dist(n=100, p=0.5, k=50)
print(test.compute_binomial()) 
print(test.compute_mu_std()) 
test.plot_chart()