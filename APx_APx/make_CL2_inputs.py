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
        apx_dict[apx_clock] = ['0x0000000000000000'] * 100
    
    #Read the yaml config
    with open("CL1_CL2_linkmap.yml", 'r') as stream:
        link_map = yaml.safe_load(stream)['link_map']
    
    for i in range(0,84):
        for board in link_map:
            filename = '{}_{}.txt'.format(list(board.keys())[0],i)
            links = list(board.values())[0]
            
            og_links = list(range(int(links.split(':')[0].split('-')[0]), int(links.split(':')[0].split('-')[1])+1))
            remapped_links = list(range(int(links.split(':')[1].split('-')[0]), int(links.split(':')[1].split('-')[1])+1))
            assert len(og_links) == len(remapped_links)
            
            print("Remapping {} to {} in {}.".format(og_links, remapped_links, filename))
            
            #Read the file in
            with open("CL1_Serenity_outputs/{}".format(filename), 'r') as istr:
                for j, line in enumerate(istr):
                    
                    if j > 3: #Skip the first 3 lines
                        emp_clock = int(line[6:10])
                        apx_clock = f"0x{emp_clock:04x}"
                        
                        #Convert link data
                        emp_data = line[11:].rstrip('\n').split()
                        
                        #Filter out the sideband data (let APx sim handle this)
                        apx_data = ['0x'+value for value in emp_data if len(value) > 4]
                        
                        #Remap
                        for l in range(0,len(og_links)):
                            apx_dict[apx_clock][remapped_links[l]] = apx_data[og_links[l]]
        
        
        #Print this all out in an APx formmatted file
        APx_filename='CL2_APx_inputs/l2_apx_SC_inputs_{}.txt'.format(i)
        
        with open(APx_filename, 'w') as ostr:
            
            #Create headers
            print("#Sideband OFF", file=ostr)
            
            #Create link lables
            print("#LinkLabel", file=ostr, end='')
            print("           LINK_00", file=ostr, end='')
            label_list = ['               LINK_{:02d}'.format(x) for x in range(1,100)]
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