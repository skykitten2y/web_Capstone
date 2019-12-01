import pandas as pd
import numpy.linalg as lin
import numpy as np

import json
import cvxpy as cp
from arch import arch_model
from statsmodels.tsa.arima_model import ARIMA

def secondfunction (price_data,num_asset,inv_time,reb_time,risk_measure):

    price_parsed = price_data

    num_asset_parsed = int(num_asset)
    inv_time_parsed = inv_time
    reb_time_parsed = reb_time
    risk_measure_parsed = risk_measure

    investment_time = float(inv_time_parsed)
    rebalancing = float(reb_time_parsed)
    totalperiod = investment_time/rebalancing

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


        history = ret[:]
        for t in range(int(totalperiod)):
            modelmu = ARIMA(history, order = (1,1,0))
            model_fit_mu = modelmu.fit(disp=0)
            output = model_fit_mu.forecast()
            predictedmu.append(output[0])
            history.append(output[0])

    #
    # Y = pd.DataFrame(rets)
    #
    # fac = pd.DataFrame(factor_parsed)
    #
    # n = len(fac)  # number of periods
    # ones = [1] * n
    # ones = pd.DataFrame(ones)
    #
    # mulist = []
    # Qlist = []
    # retlist = []
    # for i in range(10):
    #     ytrun = Y.truncate(before=i,after=i+9)
    #     factrun = fac.truncate(before=i,after=i+9)
    #     rettrun = Y.truncate(before=i+9,after=i+9)
    #     onestrun = ones.truncate(before=i, after = i+9)
    #
    #     mu, Q = FF(ytrun, factrun, onestrun)  #mu:100*1, Q:100*100
    #     mulist.append(mu)
    #     Qlist.append(Q)
    #     retlist.append(rettrun.transpose())
    #
    #
    # epsilonlist = []
    # for i in range(10):
    #
    #     epsilontrun = pd.DataFrame((retlist[i].values-mulist[i].values)**2)
    #     epsilonlist.append(epsilontrun)
    #
    #
    #
    # Xreg = {}
    # for p in range(3):
    #     Xreg[p] = [float(1)] * 9
    # Xreg = pd.DataFrame(Xreg)
    #
    #
    # Blist = []
    #
    # for i in range(100):
    #     Yreg = {}
    #     Yreg[0] = [flt]*9
    #     Yreg1 = pd.DataFrame(Yreg)
    #     for j in range(9):
    #         Yreg1[0][j] = Qlist[j+1][i][i]
    #         Xreg[1][j] = epsilonlist[j][0][i]
    #         Xreg[2][j] = Qlist[j][i][i]
    #
    #         Xt = Xreg.transpose()
    #         a = np.dot(Xt, Xreg)
    #         b = np.dot(Xt,Yreg1)
    #         coe = lin.lstsq(a, b,rcond=None)[0]
    #         B = pd.DataFrame(coe)
    #         Blist.append(B)
    #
    #
    # ########going forward
    #
    #
    # Qhat1 = {}
    # for i in range(100):
    #     Qhat1[i] = [flt]*100
    #
    # Qhat1 = pd.DataFrame(Qhat1)
    #
    # for i in range(100):
    #     Qhat1[i][i] = Blist[i][0][0] + Blist[i][0][2]*Qlist[9][i][i]
    #
    # Qhat = []
    # Qhat.append(Qhat1)
    #
    # for i in range(int(totalperiod)-1):
    #
    #     Qhat2 = {}
    #     for j in range(100):
    #         Qhat2[j] = [flt]*100
    #     Qhat2 = pd.DataFrame(Qhat2)
    #
    #     for k in range(100):
    #         Qhat2[k][k] = Blist[k][0][0] + Blist[k][0][2]*Qhat[i][k][k]
    #     Qhat.append(Qhat2)
    #
    #
    # ################## calculate mu
    # epsilonlistmu = []
    # for i in range(10):
    #     epsilontrunmu = pd.DataFrame(retlist[i].values - mulist[i].values)
    #     epsilonlistmu.append(epsilontrunmu)
    #
    # Xregmu = {}
    # for p in range(3):
    #     Xregmu[p] = [float(1)] * 9
    #     Xregmu = pd.DataFrame(Xregmu)
    #
    #
    # Blistmu = []
    #
    # for i in range(100):
    #     Yregmu = {}
    #     Yregmu[0] = [flt] * 9
    #     Yregmu1 = pd.DataFrame(Yregmu)
    #     for j in range(9):
    #         Yregmu1[0][j] = mulist[j + 1][0][i]
    #         Xregmu[1][j] = epsilonlistmu[j][0][i]
    #         Xregmu[2][j] = mulist[j][0][i]
    #
    #         Xtmu = Xregmu.transpose()
    #         amu = np.dot(Xtmu, Xregmu)
    #         bmu = np.dot(Xtmu, Yregmu1)
    #         coemu = lin.lstsq(amu, bmu, rcond=None)[0]
    #         Bmu = pd.DataFrame(coemu)
    #         Blistmu.append(Bmu)
    #
    # ###### going forward
    # muhat1 = {}
    # for i in range(100):
    #     muhat1[i] = [flt]
    #
    # muhat1 = pd.DataFrame(muhat1).transpose()
    #
    # for i in range(100):
    #     muhat1[0][i] = Blistmu[i][0][0] + Blistmu[i][0][2] * mulist[9][0][i]
    #
    #
    # muhat = []
    # muhat.append(muhat1)
    # for i in range(int(totalperiod) - 1):
    #
    #     muhat2 = {}
    #     for j in range(100):
    #         muhat2[j] = [flt]
    #     muhat2 = pd.DataFrame(muhat2).transpose()
    #
    #     for k in range(100):
    #         muhat2[0][k] = Blistmu[k][0][0] + Blistmu[k][0][2] * muhat[i][0][k]
    #     muhat.append(muhat2)



    ########## MVO
    Qmatrix = np.zeros((100 * int(totalperiod), 100 * int(totalperiod)))
    mumatrix = np.zeros((100 * int(totalperiod), 1))

    for i in range(int(totalperiod)):
        for j in range(100):
            Qmatrix[i*100+j,i*100+j] = predictedQ[j][i]


    for i in range(int(totalperiod)):
        for j in range(100):
            mumatrix[i*100+j] = predictedmu[j*int(totalperiod)+i]


    lamda = 0.12*(risk_measure_parsed/2.2361)

    Amatrix = np.zeros((100*int(totalperiod),100*int(totalperiod)))
    for i in range(int(totalperiod)):
        for j in range(100):

            if lamda*(1-(1/(30/rebalancing)*i)) >= 0:
                Amatrix[i*100+j, i*100+j] = lamda*(1-(1/(30/rebalancing)*i))
            else:
                Amatrix[i * 100 + j, i * 100 + j] = 0

    qmatrix = mumatrix.T@Amatrix
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



    prob = cp.Problem(cp.Minimize(cp.quad_form(x,Qmatrix) - qmatrix@x + cmatrix.T@z1),
                      [z <= z1,
                       -z <= z1,
                       onematrix@z == zeromatrix,
                       onemat1@x + z == onemat2@x,
                       onemat3.T@y == num_asset_parsed,
                       x <= onemat4@y,
                       onemat5.T@x == float(1)])

    prob.solve()
    weight = x.value

    for i in range(len(weight)):
        if weight[i]<0.0000001:
            weight[i]=0

    return weight































