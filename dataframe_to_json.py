from cmath import nan
import simplejson as json
import pandas as pd
import string
import sys
import requests
import time

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


def dict_to_dataframe(dict):
    return pd.DataFrame.from_dict(dict, orient ='index')

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

def return_coloumn_values(dict, header):
   
    for key in dict:
        print(dict[key][header])

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
            print(key)
    return list

#prints all the values for a given list of indexes
def print_list(dict, list):

    x = 0
    for item in list:
        print(dict[list[x]])
        x += 1

#get the farnell stock level for a given farnell part number
def get_farnell_stock_qty(part_number):

 
    url = "https://api.element14.com/catalog/products?versionNumber=1.2&term=id%3A"
    url = url + part_number
    url = url + "&storeInfo.id=uk.farnell.com&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=rohsCompliant%2CinStock&resultsSettings.responseGroup=large&callInfo.omitXmlSchema=false&callInfo.responseDataFormat=json&callinfo.apiKey=rhcf7dupd8arzxtvqubksbbw"
    response = requests.get(url)
    data = response.json()
    #print(data['premierFarnellPartNumberReturn']['products'][0]['stock']['level']) # 
    try:
        return data['premierFarnellPartNumberReturn']['products'][0]['stock']['level'] # 
    except KeyError:
        return "NOT FOUND"
  

def add_stock_levels(dict):
    list = []
    #get all the farnell stock levels
    for key in dict:
        

        if(type(dict[key]["OC_FARNELL"])is str):
            print("working...")
            list.append(get_farnell_stock_qty(dict[key]["OC_FARNELL"]))
            time.sleep(0.6) #not allowed to poll too often with Farnell
        else:
            print("N/A")
            list.append("N/A")
 #   print("list")
 #   print(list)
    #turn to a dataframe

    df = dict_to_dataframe(dict)

 #   print("list length")
 #   print(len(list))
#    print("df length")
#    print(len(df.index))
    df["FARNELL STOCK"] = list
    print(df)
    #add Farnell stock coloumn







path = sys.path[0] + "\output.csv"  #create file path from location this program is in
data_frame =pd.read_csv(path)       #read in the csv file
raw_dictionary = data_frame.to_dict(orient='index') #keep the data as a dictionary


working_data = clean_dictionary(raw_dictionary) #get rid of the data we do not want

add_stock_levels(working_data)
#return_coloumn_values(working_data, "OC_FARNELL")
#empty_mpn_list = get_empty_entries(working_data, "MPN")  #get all empty MPN entries
#print_list(working_data,empty_mpn_list)