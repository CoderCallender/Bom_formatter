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
#root.columnconfigure(0, weight=1, minsize=75)
#root.rowconfigure(0, weight=1, minsize=50)




###################################################################
def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    text_box.delete(0.0,'end')
    text_box.insert(tk.END, filename)
    

###################################################################


###################################################################
def copy():
   source_file = text_box.get(0.0,'end')
   working_file = os.path.dirname(source_file)
   print("dir")
   print(working_file)
   working_file += "/copy.csv"
   print("working file")
   print(working_file)
   source_file = source_file.strip()
   print("source file")
   print(source_file)
   if os.path.exists(working_file):
    os.remove(working_file)
   else:
    print("No file to delete.")

   #make name for new file
   
   output_file = os.path.dirname(source_file)
   output_file += "/output.csv"
   print("output file")
   print(output_file)
   # make a copy of our file
   shutil.copyfile(source_file, working_file)
   reader = csv.reader(open(working_file, "r"), delimiter=';')
   writer = csv.writer(open(output_file, 'w' , newline=''), delimiter=',')
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
    command=copy
)
#open_button.pack(expand=True)

#text_box.pack()
text_box.grid(row=0,column=1,padx=5)
browse_button.grid(row=0,column=2)
format_button.grid(row=2,column=2)
text_box.insert(tk.END, "select file")


# run the application
root.mainloop()