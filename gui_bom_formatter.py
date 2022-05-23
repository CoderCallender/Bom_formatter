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
def format():
   source_file = text_box.get(0.0,'end')    #get source file from text box
   working_file = os.path.dirname(source_file)  #get path

   working_file += "/output.csv"    #add on our new name
 
   source_file = source_file.strip()    #strip any rouge newlines

   if os.path.exists(working_file):
    os.remove(working_file)     #if old file is there, delete it
   else:
    print("No file to delete.")

   #replace the semicolons for commas into the output file
   reader = csv.reader(open(source_file, "r"), delimiter=';')   
   writer = csv.writer(open(working_file, 'w' , newline=''), delimiter=',')
   writer.writerows(reader)
###################################################################


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
    command=format
)
#open_button.pack(expand=True)

#text_box.pack()
text_box.grid(row=0,column=1,padx=5)
browse_button.grid(row=0,column=2)
format_button.grid(row=2,column=2)
text_box.insert(tk.END, "select file")


# run the application
root.mainloop()