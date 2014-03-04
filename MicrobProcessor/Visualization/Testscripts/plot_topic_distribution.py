'''
Created on 20/11/2013

author: sperez8
'''
import numpy as np

study = '1037'
#Z = range(2,22)
Z = [8]
f = '/Users/sperez/git/microbPLSA/MicrobProcessor/Results/study_'+study +'_'
end = '_topics_.txt'

format = 'pdf'
order = ['1', '12', '3', '0', '4', '5', '13', '15', '6', '7', '10', '11', '23', '9', '22', '2', '14', '17', '8', '20', '21', '19', '16', '18']
order = [int(o) for o in order]
order = np.array(order)
print order

if format == 'svg':
    import matplotlib
    matplotlib.use('SVG')
    
    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import * #have to import this AFTER selecting SVG usage.
    
    for z in Z:
        plot = topic_distribution(f+str(z)+end,study, order)
        plot.savefig('/Users/sperez/Desktop/topic_dist_'+study+'_'+str(z)+'plots.svg')
        print '\n\n\n The topic distribution svg file is ready.'

elif format == 'pdf':

    import os,sys
    _cur_dir = os.path.dirname(os.path.realpath(__file__))
    _root_dir = os.path.dirname(_cur_dir)
    sys.path.insert(0, _root_dir)
    from microbPlotter import *
    
    from matplotlib.backends.backend_pdf import PdfPages
    
    pdf = PdfPages('/Users/sperez/Desktop/topic_dist_'+study+'plots.pdf')
    
    for z in Z:
        plot = topic_distribution(f+str(z)+end,study, order)
        plot.savefig(pdf, format='pdf')
        
    pdf.close()
    print '\n\n\n The topic distribution pdf file is ready.'



