'''
Created on 29/01/2014

author: sperez8

contains a bunch of different utilities to read EMP data

'''
import numpy as np
import json
import sys, os
from math import sqrt
from scipy.stats.stats import pearsonr
from scipy.stats import chisquare


_cur_dir = os.path.dirname(os.path.realpath(__file__))
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)
import microbplsa




def topic_point_bisectoral_correlation(file,Y):
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata boolean vector Y,
     we can calculate the correlation between the topic distributions 
     and dichotomous factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of sampless
    R = []
    N
    for z in range (0,Z):
        X = p_z_d[z]
        M1 = X[Y]
        n1 = float(len(M1))
        M1 = np.mean(M1)
        M0 = X[np.logical_not(Y)]
        n0 = float(len(M0))
        M0 = np.mean(M0)
        if n1 + n0 != N: raise NameError('Something funky about your metadata: number of samples is not equal to the total of Y elements.')
        s_n = np.std(X)
        r = ((M1-M0)/s_n)*sqrt((n1*n0)/((n1+n0)**2))
        R.append(round(r,2))
   
    return R
    
def topic_pearson_correlation(file,Y):
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata boolean vector Y,
     we can calculate the correlation between the topic distributions 
     and continuous factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of sampless
    R = []
    for z in range (0,Z):
        X = p_z_d[z]
        R.append([round(x,3) for x in pearsonr(X,Y)])
   
    return R

def topic_category_correlation(file, Y):
    '''Given a model p_z,p_w_z,p_d_z, and sample metadata boolean vector Y,
     we can calculate the correlation between the topic distributions 
     and categorical factors'''
    
    m = microbplsa.MicrobPLSA()
    plsa = m.open_model(file) #get model from the results file
    p_z = plsa.p_z
    
    #return document's distribution
    p_z_d = plsa.document_topics()    
    Z,N =p_z_d.shape #number of sampless
    R = []
    for z in range(0,Z):
        f_obs = p_z_d[z]
        p_z_list = [p_z[z] for i in range (0,N)]
        R.append( chisquare(f_obs,f_exp = p_z[z]) )
    
    return R
    