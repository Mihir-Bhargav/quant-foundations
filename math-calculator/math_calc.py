import math


class math_calc():
    def __init__(self, f):
        self.f = f

    def calculate_derivative(self, x, h=1e-7):
        self.derivative = (self.f(x + h) - self.f(x - h)) / (2 * h)
        print(f"The derivative at x={x} is: {round(self.derivative, 2)}")
        return round(self.derivative, 2)

    def solve_functions(self, x0=1.0, tol=1e-10, max_iter=100, h=1e-7):
        """Find a root of f with Newton's method, starting from x0.

        The derivative is estimated with a central difference, so no
        printing happens inside the loop. Raises ValueError if the derivative
        is zero, if the iteration does not converge within max_iter steps.
        """
        x = x0
        for _ in range(max_iter):
            fx = self.f(x)
            dfx = (self.f(x + h) - self.f(x - h)) / (2 * h)
            if dfx == 0:
                raise ValueError(f"Derivative is zero at x={x}; Newton's method cannot continue.")
            step = fx / dfx
            x -= step
            if abs(step) < tol:
                return x
        raise ValueError(f"No convergence after {max_iter} iterations (last x={x}).")


if __name__ == "__main__":
    test = math_calc(lambda x: 3 * x**4)
    print(test.calculate_derivative(4))

    root = math_calc(lambda x: x**2 - 2)
    print(f"Root of x^2 - 2 from x0=1: {root.solve_functions(1.0):.10f} (sqrt(2) = {math.sqrt(2):.10f})")
