"""
Insight Data Engineering Challange

Entry for: Timothy J. Dennis
           401 Beech Lane
           Bowling Green, OH 43402
           tjdphd@gmail.com
           815-990-8591
"""

"""module h1b_util - contains functions defined for examining csv files containing data from the
                     department of labor related to H1B (H-1B,H-1B1,E-3) visa holders

"""

import sys

def replace_quote_enclosed_semi_colons(in_string):
    """seek substrings of in_string enclosed in double quotes 
       and replace semi colons contained in substring with commas

       prevents such semi-colons from causing problems
       when using split(';') on in_string to create a list"""


# assume a quote-enclosed semi-colon will be found
    sc_key                     = True

# initialize indices where opening and closing double quotes appear in in_string to 0
    dq_key_ind_close           = 0
    dq_key_ind_open            = 0

    len_in_string              = len(in_string)

# for as long as there may be a quote-enclosed semi-colon, loop over the string

    while(sc_key):

# look for the next opening double quote

        if in_string[dq_key_ind_close+1:len_in_string-1].__contains__('"'):

# if found find closing double quote
            dq_key_ind_open    =  dq_key_ind_close + 1 + in_string[dq_key_ind_close+1:len_in_string-1].index('"')
            dq_key_ind_close   = in_string.index('"',dq_key_ind_open + 1)
            sc_key             = in_string[dq_key_ind_open:dq_key_ind_close].__contains__(";")
# check double-quoted substring for presence of semi-colon
            if sc_key == True:
# if found get index of semi-colon
                sc_key_ind     = in_string[dq_key_ind_open:dq_key_ind_close].index(';') + dq_key_ind_open
# replace the semi-colon with a comma in the substring put in new substring
                old_sub_string = in_string[dq_key_ind_open:dq_key_ind_close+1]
                new_sub_string = old_sub_string.replace(";",",")
# replace the portion of in_string containing the old substring with the new substring
                in_string      = in_string.replace(old_sub_string,new_sub_string)
        else:
            sc_key             = False
    return in_string


def read_csv(input_data_path):
    """read a csv file in input_data_path and return a list 
       of dictionaries. Each dictionary corresponds to one record
       from the file. Dictionary keys are from the headers
       given in the header line of the file. Dictionary values
       correspond to the values found in the individual fields of
       the record."""

# latin-1 encoding used to avoid read errors discovered while testing

    with open(input_data_path, encoding = 'latin-1') as data_file:

# create a list of headers

        header_line         = data_file.readline()
        header_line         = header_line.split(';')

        data_list           = []
    
        line_count          = 0

# when a record contains a number of fields that differs from the number of headers an error is noted

        max_error_cnt       = 1
        error_cnt           = 0

        for line in data_file:
            line_count     += 1

# certain html character codes can cause trouble so we fix those first

            line            = line.replace("&AMP;", "&")
            line            = line.replace("&NBSP;"," ")

# some semi-colons enclosed in quotes are not intended as field seperators
# so we deal with those also

            line            = replace_quote_enclosed_semi_colons(line)

# now turn the line string into a list and create an empty dictionary

            data_line_list  = line.split(';')
            data_line_dict  = {}
 
# here we check if the number of fields in the data line list is the same as the number of headers

            if len(data_line_list) == len(header_line):

# if so we loop over the line list and add add a dictionary entry
# with the header as key and the corresponding list item as value
     
                for i_header in range(len(header_line)):
                    data_line_dict[header_line[i_header]] = data_line_list[i_header]
 
# now we append this lines dictionary to the list of dictionaries

                data_list.append(data_line_dict)
 
            else:

# if this section gets executed the code needs to be adjusted to deal with the data
# it is trying to read

                error_cnt += 1
                print("number of fields = ", len(data_line_list))
                print("data_line_list   = ", data_line_list)
                print("ERROR: number of fields does not match number of headings at line number {}".format(line_count))
                if error_cnt >= max_error_cnt:
                    exit()

        data_file.close()
  
    return data_list

def write_h1b_output(out_tups, header_string, out_path):
    """take a list of tuples and write them to an output file with some statistics
       list is assumed to be sorted and for containing more than 10 
       entries, only the top 10 are output (i.e. the first ten entries)

    :out_tups list arg1: a list of tuples of the form (str, int)
                         where str is a descriptive string such as
                         the name of a state or a type of occupation
                         and int is a number that ranks str in comparison
                         to the strings contained in other tuples of the
                         list
    :header_string:arg2: a string describing the contents of the tuple
                         entries in the list given by arg1
                         this string is used to create a header line
                         for the csv file which is output

    :out_path:arg3:      a string telling the function where to place the
                         output file in the file system
"""

# give the user some useful information and indication that the program is proceeding
    print("writing output to file: ", out_path)

# track the total number of applicants referenced based on second element of the tuples
# this allows the percentage relative to the total to be computed and included for each
# output entry 

    tot_cert_apps      = 0
    for j in range(len(out_tups)):
        tot_cert_apps += out_tups[j][1]

# if the file contains fewer than 10 entries, loop only over those entries, otherwise
# loop over the first ten entries

    k_range            = min(10,len(out_tups))
    out_file           = open(out_path,'w')

# place the header string
    out_file.write(header_string +'\n')
# place the entries
    for k in range(k_range):
        next_line      = str(out_tups[k][0]).strip('"') + ';' + str(out_tups[k][1]) + ';' + str(round(100*out_tups[k][1]/tot_cert_apps,1)) +'%\n'
        out_file.write(next_line)

    out_file.close()

    return 0

def get_full_header_name(line_dict, field_str):
    """find the actual key name among the keys in a dictionary, when
       the input string 'field_str' may be a substring of the full key name
       return the string giving the actual field name

       :line_dict:arg1: a dictionary whose keys are strings
       :field_str:arg2: a 'field string' which has been assumed to be a key in the dictionary line_dict

       E.g. if field_str = 'STATUS' but the dictionary contains a key given
            by 'CASE_STATUS', then this function will find the key 'CASE_STATUS'
            and return it as its output. 

       NOTE: if field_str is not found as a substring of any of the keys then it is returned
             unchanged and a warning is issued
"""

# get a list of the keys
    keys                     = line_dict.keys()

# check the keys until one is found containing field_str as a substring
    for key in keys:
        if key.__contains__(field_str):
            full_header_name = key
            return full_header_name
# print a warning and return the original string if an appropriate key is not found
    print("WARNING: could not find header containing \"{}\" ".format(field_str))
    return field_str

def top_10_certified_x(data_list, field_str):

    """take a list of H1B visa data from the department of labor
       and controlling for certified applications. Find all possible
       values associated with the header given by field_str, then
       find the values whose frequencies in the data are in the top ten.
       return a list of tuples whose first entry gives a value
       corresponding the the header field_str and whose second entry
       gives the number of times the value was found in the data

       :data_list:arg1: a list of dictionaries. This list is the output
        of read_csv see documentation for that function for details

       :field_str:arg2: a string giving the name of a header that is
        expected to be found as a key in the dictionaries in arg1

       E.G. if field_str is 'SOC_NAME', the function looks at each
       dictionary in arg1 and creates a list of all possible values
       corresponding to that key. The function then counts the number
       of times each of these values is found in the list. A list
       of tuples is creating giving each value and its frequency which
       is then sorted. The top ten entries are returned.

"""

# different data files have different but similar heading names. Find the correct heading names here.

    full_field_str_name      = get_full_header_name(data_list[0],field_str)
    full_status_str_name     = get_full_header_name(data_list[0],'STATUS')


# create a list of all possible values corresponding the key given by full_field_str_name

    field_list               = []

    for line_dict in data_list:
        if not line_dict[full_field_str_name] in field_list:
            field_list.append(line_dict[full_field_str_name])

# turn it into a dictionary with the field list as keys and the frequencies as values
# let initial frequency values be zero

    field_dict               = dict.fromkeys(field_list,0)

# pass through the data list again and count the number of times
# each value appears - but control for certified applicants only

    for line_dict in data_list:

        if line_dict[full_status_str_name] == 'CERTIFIED':
            field_dict[line_dict[full_field_str_name]] += 1

# turn the dictionary into a list of tuples and sort by frequency

    field_tups               = list(field_dict.items())
    field_tups.sort(key      = lambda tup: tup[1], reverse = True)

# now look for ties in frequency value and sort alphabetically among tied values

    sorted_field_tups        = []
    tied_entries             = []

    for tup in field_tups:

# get the first tup in the list

        if len(tied_entries) == 0:
            tied_entries.append(tup)
        else:

# look for a tie but control for the last entry in the tuple list

            if tied_entries[-1][1] == tup[1] and tup != field_tups[-1]:
                tied_entries.append(tup)
            else:

# if the current tuple is the last in the list and is a tie add it to the list of tied entries before sorting

                if tup == field_tups[-1] and tied_entries[-1][1] == tup[1]:
                    tied_entries.append(tup)
                    last_tup_was_a_tie = True
                else:
                    last_tup_was_a_tie = False

# some of the strings in the tuples need to be processed for a proper sort do this first before sorting

                proc_tied_entries      = []
                for temp_tup in tied_entries:

# get rid of double quotes and replace spaces with underscores 

                    proc_temp_tup      = (temp_tup[0].replace(' ','_').strip('"'),temp_tup[1])
                    proc_tied_entries.append(proc_temp_tup)

# now sort the tuples among the tied entries alphabetically

                proc_tied_entries.sort(key = lambda tp:tp[0], reverse = False)   

# now the underscores can go back to being spaces before being appended to the list containing sorted tuples

                for i in range(len(proc_tied_entries)):
                    temp_tup           = (proc_tied_entries[i][0].replace('_',' '), proc_tied_entries[i][1])
                    sorted_field_tups.append(temp_tup)
                    proc_tied_entries[i] = temp_tup

# if the current tup is not the last and was not among the tied entries, re-create tied_entries with tup as first element

                if tup != field_tups[-1]:
                    tied_entries       = []
                    tied_entries.append(tup)
                else:

# if the current tup is the last tup and was not a tie it still needs to be appended to the sorted field list

                    if last_tup_was_a_tie == False and tup == field_tups[-1]:
                        sorted_field_tups.append(tup)

    return sorted_field_tups
