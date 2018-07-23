from scipy.special import binom
from scipy.misc import comb
import numpy as np

def Bernstein(n, k):
    """Bernstein polynomial.
    """
    coeff = binom(n, k)

    def _bpoly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bpoly

def bernstein_polynomial(i, n, t):
        """
            Bernstein Polynomial function
            params:
                i: <int> order
                n: <int> degree
                t: <int> 
        """

        return comb(n, i) * (t**(n - i)) * (1 - t)**i

if __name__ == "__main__":
    t =  np.linspace(0, 1, num=10)
    poly = Bernstein(1,1)(t)
    print (poly)
    print(bernstein_polynomial(1,1, t))


