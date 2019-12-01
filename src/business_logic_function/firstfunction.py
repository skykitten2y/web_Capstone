
import numpy as np
import pandas as pd
from src.business_logic_function.FF import FF




def firstfunction (given_portfolio, price_data,factor_data,horizon):

    rebalancing = 0.5
    horizon_time = horizon
    totalperiod = horizon_time / rebalancing


    L = []
    for keys in given_portfolio.keys():
        L.append(keys)

    N = len(L)

    rets = {}
    for i in L:
        ret = []
        for j in range(len(price_data[i]) - 1):
            ret.append((price_data[i][j + 1] - price_data[i][j]) / price_data[i][j])

        rets[i] = ret


    Y = pd.DataFrame(rets)

    fac = pd.DataFrame(factor_data)

    n = len(fac)  # number of periods
    ones = [1] * n
    ones = pd.DataFrame(ones)


    ytrun = Y.truncate(before=20-totalperiod,after=20)
    factrun = fac.truncate(before=20-totalperiod,after=20)
    onestrun = ones.truncate(before=20-totalperiod, after = 20)


    mu, Q = FF(ytrun, factrun, onestrun)  #mu:100*1, Q:100*100


    Qmatrix = np.zeros((N, N))
    mumatrix = np.zeros((N, 1))

    for i in range(N):
        for j in range(N):
            Qmatrix[i,j] = Q[j][i]

    for i in range(N):
        mumatrix[i] = mu[0][i]

    weight = np.zeros((N,1))

    temp = 0
    for key in given_portfolio.keys():
        weight[temp] = given_portfolio[key]
        temp = temp + 1


    returns = mumatrix.T@weight
    risk = (weight.T@Qmatrix)@weight


    return returns, risk






