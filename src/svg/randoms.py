# -*- encoding: utf-8 -*-
# Date: 04/Jun/2023
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Description: Random values by numpy random generator
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
# from numpy.random import Generator, PCG64
import matplotlib.pyplot as plt


def random2d(center, x_scale=1, y_scale=1, factor=0, N=100):
    rng = np.random.default_rng()  # seed=12345
    cov = [[x_scale, factor], [factor, y_scale]]
    return rng.multivariate_normal(center, cov, size=(N,))


def test_multivariate():
    """ test multivariate distribution """
    # rng = np.random.default_rng(seed=12345)

    # mean = [100, 100]
    # cov = [[1, 0], [0, 1]]
    # pts = rng.multivariate_normal(mean, cov, size=(2000,))
    # print('pts=', pts, pts.shape)
    pts = random2d((100, 100), 1, 1, 0, 1000)

    x, y = pts.T
    plt.plot(x, y, 'x')
    plt.axis('equal')
    plt.show()


def test_distributions():
    """ test distribution random """
    # https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator
    rng = np.random.default_rng(seed=12345)
    # rng = np.random.default_rng()
    arr = rng.beta(5, 1, size=(5, 5))
    print('beta arr=', arr)

    arr = rng.binomial(10, 0.5, size=(10,))
    print('binomial arr=', arr)
    print('normal arr=', rng.normal(0, 1, size=(10,)))
    print('uniform arr=', rng.uniform(0, 1, size=(10,)))

    # print('multivariate_normal arr=', rng.multivariate_normal(5, 1, size=(5, 5)))
    # print('chisquare arr=', rng.chisquare(5, 1, size=(5, 5)))
    # print('dirichlet arr=', rng.dirichlet(5, 1, size=(5, 5)))
    # print('exponential arr=', rng.exponential(5, 1, size=(5, 5)))
    # print('f arr=', rng.f(5, 1, size=(5, 5)))
    # print('gamma arr=', rng.gamma(5, 1, size=(5, 5)))
    # print('geometric arr=', rng.geometric(5, 1, size=(5, 5)))
    # print('gumbel arr=', rng.gumbel(5, 1, size=(5, 5)))
    # print('hypergeometric arr=', rng.hypergeometric(5, 1, size=(5, 5)))
    # print('laplace arr=', rng.laplace(5, 1, size=(5, 5)))
    # print('logistic arr=', rng.logistic(5, 1, size=(5, 5)))
    # print('lognormal arr=', rng.lognormal(5, 1, size=(5, 5)))
    # print('logseries arr=', rng.logseries(5, 1, size=(5, 5)))
    # print('multinomial arr=', rng.multinomial(5, 1, size=(5, 5)))
    # print('multivariate_hypergeometric arr=', rng.multivariate_hypergeometric(5, 1, size=(5, 5)))
    # print('multivariate_normal arr=', rng.multivariate_normal(5, 1, size=(5, 5)))
    # print('negative_binomial arr=', rng.negative_binomial(5, 1, size=(5, 5)))
    # print('noncentral_chisquare arr=', rng.noncentral_chisquare(5, 1, size=(5, 5)))
    # print('noncentral_f arr=', rng.noncentral_f(5, 1, size=(5, 5)))
    # print('pareto arr=', rng.pareto(5, 1, size=(5, 5)))
    # print('poisson arr=', rng.poisson(5, 1, size=(5, 5)))
    # print('power arr=', rng.power(5, 1, size=(5, 5)))
    # print('rayleigh arr=', rng.rayleigh(5, 1, size=(5, 5)))
    # print('standard_cauchy arr=', rng.standard_cauchy(5, 1, size=(5, 5)))
    # print('standard_exponential arr=', rng.standard_exponential(5, 1, size=(5, 5)))
    # print('standard_gamma arr=', rng.standard_gamma(5, 1, size=(5, 5)))
    # print('standard_normal arr=', rng.standard_normal(5, 1, size=(5, 5)))
    # print('standard_t arr=', rng.standard_t(5, 1, size=(5, 5)))
    # print('triangular arr=', rng.triangular(5, 1, size=(5, 5)))
    # print('vonmises arr=', rng.vonmises(5, 1, size=(5, 5)))
    # print('wald arr=', rng.wald(5, 1, size=(5, 5)))
    # print('weibull arr=', rng.weibull(5, 1, size=(5, 5)))
    # print('zipf arr=', rng.zipf(5, 1, size=(5, 5)))


def test_np_random():
    """ test random """
    # rng = np.random.default_rng(seed=12345)
    rng = np.random.default_rng()
    # rng = Generator(PCG64())
    print('rng=', rng)

    # floats
    print("float=", rng.random())
    print("floats=", rng.random((5,)))
    arr1 = rng.random((3, 2))
    print('arr1=', arr1)

    a = -2
    b = 4
    print("floats[a,b)=", (b - a) * rng.random((5,)) + a)

    # integers
    rints = rng.integers(low=0, high=10, size=20)
    print('rints=', rints)

    # choices
    print('choice=', rng.choice(5, 3))
    print('choice=', rng.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0]))
    print('choice=', rng.choice(6, 4, p=[0.1, 0, 0.3, 0.5, 0.1, 0], replace=False))
    print('choice=', rng.choice([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 2, replace=False))

    aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
    print('choice=', rng.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3]))

    # bytes
    print('bytes=', rng.bytes(10))

    # shuffle
    arr = np.arange(10)
    rng.shuffle(arr)
    print('shuffle=', arr)

    arr = np.arange(9).reshape((3, 3))
    rng.shuffle(arr)
    print('shuffle=', arr)


def main():
    """ main function """
    # test_np_random()
    # test_distributions()
    test_multivariate()


if __name__ == "__main__":
    main()
