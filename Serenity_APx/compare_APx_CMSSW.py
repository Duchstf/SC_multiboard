import pandas as pd
import bitstring as bs

#plot setting
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from matplotlib.pyplot import cm
import mplhep as hep
plt.style.use(hep.style.ROOT)

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'medium'}
pylab.rcParams.update(params)

#line thickness
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 5

# Jet scale types
ct_scales = {'pt' : 2 ** -2,
             'etaphi' : np.pi / 720}
ct_scales['eta'] = ct_scales['etaphi']
ct_scales['phi'] = ct_scales['etaphi']

gt_scales = {'pt' : 2 ** -6,
             'etaphi' : np.pi / 2 ** 13}
gt_scales['eta'] = gt_scales['etaphi']
gt_scales['phi'] = gt_scales['etaphi']

NJETS=12

def extract_fields(df, fmt='gt'):
    assert fmt in ['ct', 'gt'], "fmt must be 'ct' or 'gt'"
    if fmt == 'ct':
        scales = ct_scales
        pt_l, pt_h = 50, 64
        eta_l, eta_h = 38, 50
        phi_l, phi_h = 27, 38
    elif fmt == 'gt':
        scales = gt_scales
        pt_l, pt_h = 48, 64
        eta_l, eta_h = 21, 35
        phi_l, phi_h = 35, 48

    bits = [bs.pack('0x' + x) for x in df.data]
    
    hwpt = np.array([b[pt_l:pt_h].uint for b in bits])
    pt = hwpt * scales['pt']
    
    hweta = np.array([b[eta_l:eta_h].int for b in bits])
    eta = hweta * scales['eta']
    
    hwphi = np.array([b[phi_l:phi_h].int for b in bits])
    phi = hwphi * scales['phi']
    df['pt'], df['eta'], df['phi'] = pt, eta, phi
    df['hwpt'], df['hweta'], df['hwphi'] = hwpt, hweta, hwphi
    return df

def distributions(APx_collection, CMSSW_collection):
    APx_df = pd.DataFrame()
    CMSSW_df = pd.DataFrame()
    
    APx_df['data'] = APx_collection
    CMSSW_df['data'] = CMSSW_collection
    
    APx_df = extract_fields(APx_df)
    CMSSW_df = extract_fields(CMSSW_df)
    
    #Plot the pT
    plt.hist(APx_df['pt'].to_numpy(), bins=20, label=r'APx $p_T$', alpha=0.8)
    plt.hist(CMSSW_df['pt'].to_numpy(), bins=20, label=r'CMSSW $p_T$', alpha=0.3)
    plt.xlabel(r'$p_T$ [GeV]')
    plt.ylabel(r'Number of Jets')
    plt.legend(loc='best')
    plt.savefig('plots/pt_dist.png')
    plt.close()
    
    #Plot eta
    plt.hist(APx_df['eta'].to_numpy(), bins=20, label=r'APx $\eta$', alpha=0.6)
    plt.hist(CMSSW_df['eta'].to_numpy(), bins=20, label=r'CMSSW $\eta$', alpha=0.6)
    plt.xlabel(r'$\eta$')
    plt.ylabel(r'Number of Jets')
    plt.legend(loc='best')
    plt.savefig('plots/eta_dist.png')
    plt.close()
    
    #Plot phi
    plt.hist(APx_df['phi'].to_numpy(), bins=20, label=r'APx $\phi$', alpha=0.6)
    plt.hist(CMSSW_df['phi'].to_numpy(), bins=20, label=r'CMSSW $\phi$', alpha=0.6)
    plt.xlabel(r'$phi$')
    plt.ylabel(r'Number of Jets')
    plt.legend(loc='best')
    plt.savefig('plots/phi_dist.png')
    plt.close()
    
def bit_to_bit(APx_collection, CMSSW_collection):
    '''
    Look at the jet outputs from both CMSSW and APx boards, compare them bit to bit.
    '''
    
    num_matched_jets = 0
    num_unmatched_jets = 0
    
    for i in range(min(len(APx_collection),len(CMSSW_collection))):
        print('Jet index {}.'.format(i))
        print('APx Jet Output: ', APx_collection[i])
        print('CMSSW Jet Output: ', CMSSW_collection[i])
        print('Equal: {}'.format(APx_collection[i] == CMSSW_collection[i]))
        print('------------')
        
        if APx_collection[i] == CMSSW_collection[i]:
            num_matched_jets += 1
        else:
            num_unmatched_jets += 1
    
    #Plot the bit matching
    fig, ax = plt.subplots()
    
    y_pos = np.asarray([0, 1])
    num_jets = np.asarray([num_matched_jets, num_unmatched_jets])
    num_labels = ['Matched', 'Un-matched']

    hbars = ax.barh(y_pos, num_jets, align='center')
    ax.set_yticks(y_pos, labels=num_labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of jets')
    ax.set_title('bit-by-bit matching')

    # Label with given captions, custom padding and annotate options
    ax.bar_label(hbars)
    ax.set_xlim(right=max(num_jets)*1.2)

    plt.savefig('plots/bit_matching_1file.pdf', bbox_inches='tight')
    

def main():
    pass

    #Number of files
    N=0
    
    APx_collection = []
    CMSSW_collection = []
    
    for i in range(0,N+1):
        #Get APx output 
        with open("l2_apx_SC_outputs_{}.txt".format(i), 'r') as apx:
            for j, line in enumerate(apx):
                if j > 2: #Ignore the first 2 lines
                    jet = line[16:].rstrip('\n').split()
                    if len(jet) > 0 and jet[0][2:] != '0000000000000000':    
                        APx_collection += [jet[0][2:].lower()] #Ignore the 0x part 
                    
                    
        with open("CL2_CMSSW_outputs/L1CTSCJetsPatterns_{}.txt".format(i), 'r') as cmssw:
            for j, line in enumerate(cmssw):
                if j > 3: #Ignore the first 2 lines
                    jet = line[19:].rstrip('\n').split()
                    if len(jet) > 0 and jet[0] != '0000000000000000':    
                        CMSSW_collection += jet #Ignore the 0x part 
    
    #bit_to_bit(APx_collection, CMSSW_collection)
    distributions(APx_collection, CMSSW_collection)
    
main()