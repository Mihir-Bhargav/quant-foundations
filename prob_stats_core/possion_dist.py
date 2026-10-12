import matplotlib.pyplot as plt 
import math

# The possion distribution is used when we know the mean, and want to find out the probability of a certain number of times an events will take place. 
# So let's say that a small business recives, on average 12 customers per day. What is the probability that is recieves exactly 8 in a day? 

# We can use this formula to find out; 
# p(X = x) = (mu ^x e^-mu)/x! => p(X=8) = 12^8(e^-12)/8! which approximates to 6.55% 


class possion_dist(): 
    def __init__(self):
        pass

    def calculate_possion_distribution(self, mu, x): 
        xmin = 0 
        xmax = int(mu + 4*math.sqrt(mu))
        for x in range(xmin, xmax +1): 
            px = ((mu ** x)*(math.e**(-mu)))/ math.factorial(x)
            px = 100 * px 
            print(f"The probability for P(X=x) is {round(px, 2)}%")  
        return px 

test = possion_dist() 
test.calculate_possion_distribution(10, 9)  


    