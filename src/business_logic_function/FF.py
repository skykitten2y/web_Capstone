import numpy.linalg as lin
import pandas as pd
import numpy as np


def geomean(it):
    a = np.array(it)
    a = a + 1
    return a.prod()**(1.0/len(a))-1


def FF(ret, fac,onestrun):
    num_asset = len(ret.keys())  #number of asset
    n = len(fac)                    #number of periods

    x = pd.concat([onestrun, fac], axis=1)
    x_t = x.transpose()
    a = np.dot(x_t,x)
    b = np.dot(x_t,ret)

    coe = lin.lstsq(a, b,rcond=None)[0]
    newcoe = pd.DataFrame(coe)  #alpha and beta


    faclist = []
    for key in fac.keys():
        geo = geomean(fac[key])
        faclist.append(geo)

    fbar = pd.DataFrame(faclist)

    oneaa = pd.DataFrame([float(1)])
    newfbar = pd.concat([oneaa, fbar], axis=0)

    coe_trans = newcoe.transpose()

    mu = np.dot(coe_trans, newfbar)
    mu = pd.DataFrame(mu)


    ab = pd.DataFrame(np.dot(x, newcoe))
    e = pd.DataFrame(ret.values - ab.values)

    f = fac.cov()

    d = pd.DataFrame(np.zeros(shape=(num_asset, num_asset)))

    for key in d.keys():
        d[key][key] = np.sum(np.square(e[key]))

    beta = newcoe.drop(0,axis = 0)


    Q = np.dot(beta.transpose(),f)
    Q = np.dot(Q,beta)

    Q = pd.DataFrame(Q)
    Q = pd.DataFrame(Q.values + d.values)

    return mu, Q

