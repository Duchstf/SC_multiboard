
def main():
    '''
    Look at the jet outputs from both CMSSW and APx boards, compare them.
    '''
    
    #Number of files
    N=0
    
    APx_collection = []
    CMSSW_collection = []
    
    for i in range(0,N+1):
        #Get APx output 
        with open("CL2_APx_outputs/l2_apx_SC_output_{}.txt".format(i), 'r') as apx:
            for j, line in enumerate(apx):
                if j > 2: #Ignore the first 2 lines
                    jet = line[13:].rstrip('\n').split()
                    if len(jet) > 0 and jet[0][2:] != '0000000000000000':    
                        APx_collection += [jet[0][2:].lower()] #Ignore the 0x part 
                    
                     
                 
        with open("CL2_CMSSW_outputs/L1CTSCJetsPatterns_{}.txt".format(i), 'r') as cmssw:
            for j, line in enumerate(cmssw):
                if j > 3: #Ignore the first 2 lines
                    jet = line[19:].rstrip('\n').split()
                    if len(jet) > 0 and jet[0] != '0000000000000000':    
                        CMSSW_collection += jet #Ignore the 0x part 
    
    #Bit to bit matching
    print(len(APx_collection))
    print(len(CMSSW_collection))
    
    print(APx_collection)
    print(CMSSW_collection)
    
    for i in range(min(len(APx_collection),len(CMSSW_collection))):
        print('Jet index {}.'.format(i))
        print('APx Jet Output: ', APx_collection[i])
        print('CMSSW Jet Output: ', CMSSW_collection[i])
        print('Equal: {}'.format(APx_collection[i] == CMSSW_collection[i]))
        print('------------')
    
    #Plot the distributions
    
    
main()