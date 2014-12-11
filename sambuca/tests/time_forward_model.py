import sambuca
from scipy.io import loadmat
import timeit


if __name__ == '__main__':
    '''Simple script for testing the optimisation
    experiments on the forward model.
    '''

    data = loadmat('./data/forwardModelTestValues.mat', squeeze_me=True)

    def forward_model():
        return sambuca.forward_model(
            chl=data['chl'],
            cdom=data['cdom'],
            tr=data['tr'],
            h=data['h'],
            q=data['q'],
            substrate1=data['substrate1'],
            substrate2=data['substrate2'],
            wav=data['wav'],
            awater=data['awater'],
            aphy_star=data['aphy_star'],
            d_wls=data['d_wls'],)

    iterations = 10000
    t = timeit.Timer("forward_model()", "from __main__ import forward_model")
    print(
        "Forward model, {0} iterations:     {1}".format(
            iterations,
            t.timeit(iterations)))
