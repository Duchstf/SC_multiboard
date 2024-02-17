import yaml

def main():
    
    '''
    Merge Serenity CL1 output files to produce APx CL2 input files.
    '''
    
    #Dictionary to write to apx file
    apx_dict={}
    
    #Create data entries for each clock
    for clock in range(0,1024): #Each file holds maximum 1024 clocks
        apx_clock = f"0x{clock:04x}"
        apx_dict[apx_clock] = ['0x0000000000000000'] * 6
    
    for i in range(0,1):
        #Input file name
        filename = 'CL1_out_{}.txt'.format(i)
        
        #Read the file in
        with open("CL1_APx_barrel_outputs/{}".format(filename), 'r') as istr:
            for j, line in enumerate(istr):
                
                if j > 1: #Skip the first 2 lines
                    stripped_line =  list(line.rstrip('\n').split())
                    if len(stripped_line) > 0:
                        clock = stripped_line[0]
                        
                        #Convert link data
                        data = stripped_line[1:]
                        
                        apx_dict[clock] = data
        
        #Print this all out in an APx formmatted file
        APx_filename='CL2_APx_inputs/CL2_input_{}.txt'.format(i)
        
        with open(APx_filename, 'w') as ostr:
            
            #Create headers
            print("#Sideband OFF", file=ostr)
            
            #Create link lables
            print("#LinkLabel", file=ostr, end='')
            print("           LINK_00", file=ostr, end='')
            label_list = ['               LINK_{:02d}'.format(x) for x in range(1,6)]
            print(''.join(label_list), file=ostr)
            
            print("#BeginData", file=ostr)
            
            #Write data to links
            #Loop through the dictionary created
            for key in list(apx_dict.keys()):
                data_printed = [key]
                data_printed += apx_dict[key]
                
                # Join the values back into a string with spaces
                data_printed = '    '.join(data_printed)
                print(data_printed, file=ostr)

                    
main()