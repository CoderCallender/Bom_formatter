from cmath import nan
import simplejson as json
import pandas as pd
import string
import sys
import xlsxwriter
from itertools import chain

#returns a new dictionary that only has the values we want (described by the list "wanted_data")
#dict_to_csv(working_data)  #example dump to csv
def clean_dictionary(raw_dictionary):
    wanted_data = ["Qty","Value","Device","Package","Parts","Description","MF","MPN","OC_MOUSER","OC_FARNELL","OC_DIGIKEY","ALT1","ALT_1"]
    new_dictionary = {}

    for key in raw_dictionary:

        new_dictionary[key] = {}

        for item in raw_dictionary[key]:
           #print(item)       #list of all the items in our dictionary
            
          # for x in raw_dictionary[key][item]:    
            if item in wanted_data:
                new_dictionary[key][item] = raw_dictionary[key][item]
                #   print(item)
                #header/title is to stay
    #print(new_dictionary)
    return new_dictionary
  
#Take a python dictonary data set and dump it to a .csv file
def dict_to_csv(dict):
    df = pd.DataFrame.from_dict(dict, orient="index")
    path = sys.path[0] + "\clean_bom.csv"
    df.to_csv(path)

#convert dictionary to json file
#dict_to_json(working_data) #example dump to json
def dict_to_json(dict):
    path = sys.path[0] + "\output.json"
    with open(path, "w") as outfile:
        json.dump(dict, outfile, indent=4, ignore_nan=True)

def check_farnell_stock(dict):
    for key in dict:
        #print(dict[key]["OC_FARNELL"])
        if(type(dict[key]["OC_FARNELL"]) is str):
            print("hello")
            dict[key] = "FARNELL STOCK"
           # dict[key]["FARNELL STOCK"] = "checked"
            print(dict[key])
    
    return(dict)



#return a list of all the values for a given item request
#example get all the manufacturers as a list
#manu_list = get_all_values(working_data, "MF")

#x = 0
#for val in manu_list:
#    print(x)
#    print(manu_list[x])
 #   x += 1
def get_all_values(dict, item_to_list):
    #create list
    list = []
    for key in dict:
        for item in dict[key]:
            if item in item_to_list:
                list.append(dict[key][item])
                #print(dict[key][item])
    return list


#accepts the header to be searched and the term to look for
#returns the indexs where the search term is found
#example:
#index_list = get_index(working_data , "MF", "KEMET")
def get_index(dict, search_header, search_term):
        #create list
    list = []
   # print(search_term)
    for key in dict:
     #   print(dict[key][search_header])
     #   print(type(dict[key][search_header]))
     if(type(dict[key][search_header]) is str):
        if search_term in dict[key][search_header] or dict[key][search_header] in search_term:
            list.append(key)
            #print(key)
    return list

#get all the entries in a given header that are empty
def get_empty_entries(dict, search_header):
        #create list
    list = []
   # print(search_term)
    for key in dict:
     #   print(dict[key][search_header])
     #   print(type(dict[key][search_header]))
     if(type(dict[key][search_header]) is not str):
            list.append(key)
           # print(key)
    return list

#prints all the values for a given list of indexes
def print_list(dict, list):

    x = 0
    for item in list:
        print(dict[list[x]])
        x += 1

#return a new dictionary that has a particular list that we want
def index_to_row(dict, list):

    new_dictionary = {}
    x = 0
    for item in list:
        new_dictionary[x] = dict[list[x]]
       # print(new_dictionary[x])
        x += 1    

    return new_dictionary

#outputs a list to excel file
def list_to_xlsx_sheet(list):

    path = sys.path[0] + "\\test.xlsx"
    df = pd.DataFrame(list)

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='list')
    df.to_excel(writer, sheet_name='list2') #example of saving a new sheet. Must all be done at the same time
    writer.save()

#outputs a dictionary to excel file
def dict_to_xlsx(dict):

    path = sys.path[0] + "\\test.xlsx"
    df = pd.DataFrame.from_dict(dict, orient="index")

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

#searches through a dictionary for duplicates under a given header (eg: duplicate_farnell_numbers = search_duplicates(working_data, "OC_FARNELL"))
def search_duplicates(dict, search_header):

    simple_dict = {}
    output_dict = {}
    #make a simple dictionary of the values
    for key in dict:
       # print(dict[key]["Value"])
        simple_dict[key] = str(dict[key][search_header]).lower()  #creates a dictionary of only the "search_header" values (simplifies the depth of the data)
        
    #groups the dictionary by the value istead of the key, which then puts duplicates together
    rev_dict = {}
    for key, value in simple_dict.items():
        rev_dict.setdefault(value, set()).add(key)
    #print(rev_dict)

    #save the duplicate keys into a new dictionary
    for key, values in rev_dict.items():
        if (len(values) > 1):
            #print(rev_dict[key])
            output_dict[key] = rev_dict[key]

    print(output_dict)

path = sys.path[0] + "\output.csv"  #create file path from location this program is in
data_frame =pd.read_csv(path)       #read in the csv file
#data_frame = data_frame.where(pd.notnull(data_frame), none)        #replace NaN with none
raw_dictionary = data_frame.to_dict(orient='index') #keep the data as a dictionary


working_data = clean_dictionary(raw_dictionary) #get rid of the data we do not want

#empty_mpn_list = get_empty_entries(working_data, "MPN")  #get all empty MPN entries
#print_list(working_data,empty_mpn_list)

#empty_manufacturers = index_to_row(working_data , empty_mpn_list)
#search_duplicates(working_data, "OC_FARNELL")
#dict_to_xlsx(empty_manufacturers)
#dict_to_json(empty_manufacturers)
#dict_to_xlsx(working_data)
#list_to_xlsx_sheet(empty_mpn_list)
working_data = check_farnell_stock(working_data)
dict_to_xlsx(working_data)