import pandas as pd
import numpy.linalg as lin
import numpy as np

import json

import cvxpy as cp
from arch import arch_model
from statsmodels.tsa.arima_model import ARIMA


def thirdfunction (price_data,num_asset,inv_time,reb_time,risk_measure, return_goal):

    price_parsed = price_data

    num_asset_parsed = int(num_asset)
    inv_time_parsed = inv_time
    reb_time_parsed = reb_time

    investment_time = float(inv_time_parsed)
    rebalancing = float(reb_time_parsed)
    totalperiod = investment_time / rebalancing


    return_goal = float(return_goal)/100

    flt = float(0)

    l = []
    for key in price_parsed.keys():
        l.append(key)

    rets = {}
    predictedQ = []
    predictedmu = []
    for i in l:
        ret = []
        for j in range(len(price_parsed[i]) - 1):
            ret.append((price_parsed[i][j + 1] - price_parsed[i][j]) / price_parsed[i][j])

        rets[i] = ret
        model = arch_model(ret,vol='GARCH',p=1,q=1,rescale=False)
        model_fit = model.fit()
        yhat = model_fit.forecast(horizon = int(totalperiod))
        predictedQ.append(yhat.variance.values[-1])


        modelmu = ARIMA(ret, order = (1,1,0))
        model_fit_mu = modelmu.fit(disp=0)
        output = model_fit_mu.forecast(int(totalperiod),alpha=0.05)
        predictedmu.append(output[0])



    ########## MVO
    Qmatrix = np.zeros((100 * int(totalperiod), 100 * int(totalperiod)))
    mumatrix = np.zeros((100 * int(totalperiod), 1))

    for i in range(int(totalperiod)):
        for j in range(100):
            Qmatrix[i*100+j,i*100+j] = predictedQ[j][i]


    for i in range(int(totalperiod)):
        for j in range(100):
            mumatrix[i*100+j] = predictedmu[j][i]

    lamda = 0.12 * (float(risk_measure) / 2.2361)

    Amatrix = np.zeros((100 * int(totalperiod), 100 * int(totalperiod)))
    for i in range(int(totalperiod)):
        for j in range(100):

            if lamda * (1 - (1 / (30 / rebalancing) * i)) >= 0:
                Amatrix[i * 100 + j, i * 100 + j] = lamda * (1 - (1 / (30 / rebalancing) * i))
            else:
                Amatrix[i * 100 + j, i * 100 + j] = 0

    qmatrix = mumatrix.T @ Amatrix

    mumatrix_mat = np.zeros((int(totalperiod), 100 * int(totalperiod)))
    for i in range(int(totalperiod)):
        for j in range(100):
            mumatrix_mat[i, i * 100 + j] = mumatrix[i * 100 + j]

    mumatrix_mat1 = np.zeros((int(totalperiod), 100 * int(totalperiod)))
    for i in range(int(totalperiod)):
        for j in range(100):
            mumatrix_mat1[i, i * 100 + j] = mumatrix[i * 100 + j] - (((Qmatrix[i*100+j, i*100+j]) ** (0.5)) * 0.43827)

    return_goal_mat = np.zeros((int(totalperiod)))
    for i in range(int(totalperiod)):
        return_goal_mat[i] = ((1 + return_goal) ** (1 / totalperiod)) - 1



    cmatrix = np.ones((100*(int(totalperiod)-1),1))*0.5  #####need to specify c (0.5)

    onematrix = np.zeros((int(totalperiod)-1, 100*(int(totalperiod)-1)))
    for i in range(int(totalperiod)-1):
        for j in range(100):
            onematrix[i,i*100+j] = float(1)



    zeromatrix = np.zeros((int(totalperiod)-1))

    onemat1 = np.zeros((100*(int(totalperiod)-1),100*int(totalperiod)))
    for i in range(100*(int(totalperiod)-1)):
        onemat1[i][i] = float(1)

    onemat2 = np.zeros((100*(int(totalperiod)-1),100*int(totalperiod)))
    for i in range(100*(int(totalperiod)-1)):
        onemat2[i][100+i] = float(1)

    onemat3 = np.ones((100,1))
    onemat4 = np.zeros((100*int(totalperiod),100))
    for i in range(int(totalperiod)):
        for j in range(100):
            onemat4[i*100+j][j] = float(1)

    onemat5 = np.zeros((100*int(totalperiod),1))
    for i in range(100):
        onemat5[i] = float(1)

    x = cp. Variable(100*int(totalperiod),nonneg=True)       ### 1 to T
    y = cp. Variable(100, boolean=True)
    z = cp.Variable(100*(int(totalperiod)-1))
    z1 = cp.Variable(100*(int(totalperiod)-1))    ### 1 to T-1


    prob = cp.Problem(cp.Minimize(cp.quad_form(x,Qmatrix) -qmatrix@x + cmatrix.T@z1),
                      [z <= z1,
                       -z <= z1,
                       onematrix@z == zeromatrix,
                       onemat1@x + z == onemat2@x,
                       onemat3.T@y == num_asset_parsed,
                       x <= onemat4@y,
                       onemat5.T@x == float(1),
                       mumatrix_mat@x >= return_goal_mat
                       ])

    prob.solve()
    weight = x.value

    for i in range(len(weight)):
        if weight[i]<0.0000001:
            weight[i]=0

    xr = cp.Variable(100 * int(totalperiod), nonneg=True)  ### 1 to T
    yr = cp.Variable(100, boolean=True)
    zr = cp.Variable(100 * (int(totalperiod) - 1))
    z1r = cp.Variable(100 * (int(totalperiod) - 1))


    probr = cp.Problem(cp.Minimize(cp.quad_form(xr, Qmatrix) - qmatrix @ xr + cmatrix.T @ z1r),
                       [zr <= z1r,
                        -zr <= z1r,
                        onematrix @ zr == zeromatrix,
                        onemat1 @ xr + zr == onemat2 @ xr,
                        onemat3.T @ yr == num_asset_parsed,
                        xr <= onemat4 @ yr,
                        onemat5.T @ xr == float(1),
                        mumatrix_mat1 @ xr >= return_goal_mat
                        ])

    probr.solve()
    weightr = xr.value

    for i in range(len(weightr)):
        if weightr[i] < 0.0000001:
            weightr[i] = 0


    return weight,weightr