import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import shutil
import os
import csv

# create the root window
root = tk.Tk()
root.title('BoM Formatter V1.0')
root.resizable(False, False)
root.geometry('700x150')

text_box = Text(root, height = 1, width = 75, wrap=NONE)

class file_names:
    source_file = ""
    working_file = ""


#FUNCTIONS
def check_header_valid(string):

    wanted_cols = ["Qty","Value","Device","Package","Parts","Description","MF","MPN","OC_MOUSER","OC_FARNELL","OC_DIGIKEY","ALT1","ALT_1"]

    for x in wanted_cols:
        if x in string:
            #header/title is to stay
            return True
    
    #unwanted header
    return False




###################################################################
#
#   Browse button function
#
###################################################################
def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=r'C:\Users\Chase\Desktop\Bom_formatter\Bom_formatter',
        filetypes=filetypes)

    text_box.delete(0.0,'end')
    text_box.insert(tk.END, filename)
    

###################################################################


###################################################################
#
#   Format the file
#
###################################################################
def format(file_names):
   file_names.source_file = text_box.get(0.0,'end')    #get source file from text box
   file_names.working_file = os.path.dirname(file_names.source_file)  #get path

   file_names.working_file += "/output.csv"    #add on our new name
 
   file_names.source_file = file_names.source_file.strip()    #strip any rouge newlines

   if os.path.exists(file_names.working_file):
    os.remove(file_names.working_file)     #if old file is there, delete it
   else:
    print("No file to delete.")

   #replace the semicolons for commas into the output file
   reader = csv.reader(open(file_names.source_file, "r"), delimiter=';')   
   writer = csv.writer(open(file_names.working_file, 'w' , newline=''), delimiter=',')
   writer.writerows(reader)
   
   #copy to a xlsm file
  # output = os.path.dirname(file_names.source_file)  #get path
 #  output += "/output."    #add on our new name
  # shutil.copyfile(file_names.working_file, output)

 
            
###################################################################

files = file_names()
# browse button
browse_button = ttk.Button(
    root,
    text='Browse',
    command=select_file
)

# format button
format_button = ttk.Button(
    root,
    text='format',
    command=lambda: format(files)
)
#open_button.pack(expand=True)

#text_box.pack()
text_box.grid(row=0,column=1,padx=5)
browse_button.grid(row=0,column=2)
format_button.grid(row=2,column=2)
text_box.insert(tk.END, "select file")


# run the application
root.mainloop()