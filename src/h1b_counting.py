"""
Insight Data Engineering Challange

Entry for: Timothy J. Dennis
           401 Beech Lane
           Bowling Green, OH 43402
           tjdphd@gmail.com
           815-990-8591
"""

"""h1b_count - read department of labor files containing data on h1b visa applicants
               examine the data to find the top ten occupations among certified
               applicants and the top ten states where work is to be carried out
               by certified applicants. Write the top ten list for each case
               along with corresponding frequencies for each and a percentage
               value relative to total number of certified applicants.
"""

# functions defined in h1b_util do most of the work

import h1b_util as hutil
import sys

""" Get the argument list and assign as follows:

    input_data_path:          full path name for data file to be read in
    output_top_occ_data_path: full path name for top occupations output
    output_top_sts_data_path: full path name for top states output
"""

input_data_path          = str(sys.argv[1])
output_top_occ_data_path = str(sys.argv[2])
output_top_sts_data_path = str(sys.argv[3])

# read the file into the list of dictionaries given by data_list
data_list                = hutil.read_csv(input_data_path)

# send the data_list to the function that returns the top ten frequencies
# for the field entered, in this case the occupation name

occ_tups                 = hutil.top_10_certified_x(data_list, 'SOC_NAME')

# write a header string for the csv file to be output
occ_header_string        ='TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'

# write the output to a file with header string as top line

hutil.write_h1b_output(occ_tups, occ_header_string, output_top_occ_data_path)

# Now do something similar for the top ten states. 

""" data files for different years have different headers for the state where work is to be done
    NOTE: E.g. fiscal year 2015 and 2016 has header 'WORKSITE_STATE' but fiscal year 2014 has
          headers 'WORKLOC1_STATE' and 'WORKLOC2_STATE'. in this exercise I am assuming
          the former since many entries are blank or identical for 'WORKLOC2_STATE'
"""

work_state_string        = hutil.get_full_header_name(data_list[0],'WORKSITE_STATE')

if 'WORKSITE_STATE' in data_list[0]:
    work_state_string    = 'WORKSITE_STATE'
else:
    work_state_string    = hutil.get_full_header_name(data_list[0],'WORKLOC1_STATE')

st_tups                  = hutil.top_10_certified_x(data_list, work_state_string)
st_header_string         = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
hutil.write_h1b_output(st_tups, st_header_string, output_top_sts_data_path)

