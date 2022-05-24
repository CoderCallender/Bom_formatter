import json
import pandas as pd
import string

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
    print(new_dictionary)
    with open('C:\\Users\\callende\\Desktop\\Bom_formatter\\output.json', "w") as outfile:
        json.dump(new_dictionary, outfile, indent=4)
  
        





data_frame =pd.read_csv(r'C:\Users\callende\Desktop\Bom_formatter\output.csv')
#print(df)
#data_frame.to_json(r'C:\Users\callende\Desktop\Bom_formatter\output.json', orient='index')    #output to json file
dictionary = data_frame.to_dict(orient='index') #keep the data as a dictionary

#print(data_frame.loc[20])
#print(dictionary[5]["Value"])   #example how to access an element


#print(dictionary[5])   #print out list number 5
#del dictionary[5]["Item"]   #delete this value

#print() #newline for clarity
#print again to check if deleted
#print(dictionary[5])   #print item
clean_dictionary(dictionary)
#print(dictionary)

