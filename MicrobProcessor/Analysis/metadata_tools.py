'''
Created on 18/02/2014

author: sperez8

contains a bunch of different utilities to read and organize metadata
'''

import csv
import json
import numpy as np
import string

def get_metadata(csvfile):
    '''returns metadata from csv file as an array'''
    with open(csvfile, 'rU') as file:
        spamreader = csv.reader(file, delimiter=',', quotechar='|')
        header = spamreader.next()
        x = [spamreader.next(),spamreader.next()]
        x = np.array(x)
        for row in spamreader:
            x = np.append(x,[row], axis = 0)
    return header, x

def reorder_metadata(datafile,metadata,study):
    '''gets the order of the sample names in the .biom data file. 
    Reorders the metadata in the table according to that sample order.'''
    
    #FIrst get the sample order
    json_data=open(datafile)
    data = json.load(json_data)
    json_data.close()
    columns = data['columns']
    samples = {}
    i=0
    for item in columns:
        sample_name = item['id']
        if study == '1037':
            s = str(sample_name).split('.')
            s.pop() #remove numerical id with pop()
            sample_name = '.'.join(s) 
        samples[sample_name] = i
        i+=1
    #Now we reconstruct the metadata numpy array by putting the rows in the right order.
    metatable = np.ndarray(shape=metadata.shape, dtype='S40')
    i = 0
    for x in metadata[:,0]:
        j = samples[x]
        metatable[j,:] = metadata[i,:]
        i+=1
    return metatable


def organize_metadata(metatable, factors):
    '''organizes the metadata by type in a dictionary of the form:
        {factor_type: {factor: values}} where factor_type is 
        dichotomous, continuous, categorical or simple when the 
        value of the factor is invariable'''
    N = metatable.shape[0] #number of samples
    factor_types = {"dichotomous":[], "continuous":[], "categorical":[], "constant":[]}
    #we first create a dictionary of {factor: possible values}
    for index, factor in enumerate(factors):
        column = metatable[:,index]
        options = []
        for value in column:
            if is_numerical(value):
                type = "continuous"
            else:
                if value not in options:
                    options.append(value)
        if options:
            if len(options) == N:
                type = 'constant'
            elif len(options)==2:
                type = 'dichotomous'
            elif len(options) > 2:
                type = 'categorical'
            else:
                type = 'constant'
        #print index, factor, len(options), options
        factor_types[type].append({factor:options})
    return factor_types

def sort_metadate_types(factors):
    factors_sorted = {}
    return factors_sorted

def is_numerical(value):
    '''return True if a metadata value is numerical.
        if it's 'none' then we can't tell
        if it has punctuation such as '-' or '/' 
        then it might be a range or a date'''
    
    if value == "none" or value == "None":
        return True
    elif any((char in string.letters) for char in value):
        return False
    else:
        for p in string.punctuation:
            if p in value:
                if p =='.': #probably have a float
                    pass
                elif p == '/': value = value.split(p)[-1] #probably a date...
                elif p == '-': value = value.split(p)[-1]
                else: print "I don't know how to deal with this punctuation: ", p
        try:
            v = float(value)
            return v
        except ValueError:
            return None
    
    
    
    
    
    
    