from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import *
import os
import laspy


class Uitkinter(Tk):


    def __init__(self, *args, **kwargs):
        
        # Create Tk
        super().__init__(*args, **kwargs)

        # Intitializing variables
        self.title('las2laz')
        self.dir_in = ""
        self.dir_out = ""
        self.cancel_press = False

        # Create window
        self.resizable(False, False)

        # Input dir
        self.label_in_dir = ttk.Label(text="Input dir: ")
        self.button_in_dir = ttk.Button(text='Select', command=self.select_dir_in)

        # Output dir
        self.label_out_dir = ttk.Label(text="Output dir: ")
        self.button_out_dir = ttk.Button(text='Select', command=self.select_dir_out)
            
        # Save in the same dir button
        self.label_same_dir = ttk.Label( text="Save in the same dir")
        self.same_dir = BooleanVar()
        self.buttom_same_dir = ttk.Checkbutton(variable=self.same_dir, onvalue=True, offvalue=False, command=self.same_dir_func)

        # Delete original files button
        self.label_delete_files = ttk.Label( text="Delete original files")
        self.delete_files = BooleanVar()
        self.butoom_delete_files = ttk.Checkbutton(variable=self.delete_files, onvalue=True, offvalue=False)

        # Start process
        self.start_buttom = ttk.Button(text="Start", command=self.start_process)
        
        # Cancel process 
        self.cancel = BooleanVar()
        self.cancel_buttom = ttk.Button(text="Cancel", command=self.cancel_process, state='disable')

        # Information
        self.information = ttk.Label(text="")

        # Progress bar
        self.progressbar = ttk.Progressbar(self, orient='horizontal', value=0, maximum=100, mode='determinate')

        # Define the geometry of the content in the GUI
        self.label_in_dir.grid(column=1, row=1, sticky="nsew")
        self.button_in_dir.grid(column=2, row=1, sticky="nsew")
        self.label_out_dir.grid(column=1, row=2, sticky="nsew")
        self.button_out_dir.grid(column=2, row=2, sticky="nsew")
        self.label_same_dir.grid(column=1, row=3, sticky="nsew")
        self.buttom_same_dir.grid(column=2, row=3, sticky="nsew")
        self.label_delete_files.grid(column=1, row=4, sticky="nsew")
        self.butoom_delete_files.grid(column=2, row=4, sticky="nsew")
        self.start_buttom.grid(column=3, row=7, sticky="nsew")
        self.cancel_buttom.grid(column=4, row=7, sticky="nsew")
        self.progressbar.grid(column=1, row=7, sticky="nsew")
        self.information.grid(column=1, row=8, sticky="nsew")

        # This is done to have padding around all widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=2)


    def select_dir_in(self):
        self.dir_in = fd.askdirectory(title='Select directory', initialdir='./', mustexist=True)


    def select_dir_out(self):
        self.dir_out = fd.askdirectory(title='Select directory', initialdir='./', mustexist=True)


    def same_dir_func(self):
        if self.same_dir.get() == True:
            self.button_out_dir["state"] = "disable"
        else:
            self.button_out_dir["state"] = "normal"


    def start_process(self):

        # Correct dir_out
        if self.same_dir.get() == True:
            self.dir_out = self.dir_in

        # Check inputs
        if not os.path.isdir(self.dir_in):
            self.information.configure(text="Incorrect dir in")


        elif not os.path.isdir(self.dir_out):
            self.information.configure(text="Incorrect dir out")

        # Start process
        else:
            # Updating start and cancel buttoms
            self.start_buttom.configure(state="disable")
            self.cancel_buttom.configure(state="normal")
            self.information.configure(text="Working")
            self.update()
            self.las2laz(self.dir_in, self.dir_out, self.delete_files.get())


    def cancel_process(self):
        self.cancel_press = True
        self.cancel_buttom.configure(state="disable")
        self.start_buttom.configure(state="normal")
        self.information.configure(text="Canceled")
    

    def las2laz(self, dir_in, dir_out, delete_files):
        
        dir_in = self.dir_in
        dir_out = self.dir_out
        delete_files = self.delete_files.get()

        # Extension in and out
        extension_in = '.las'
        extension_out = '.laz'

        # All dirs in dir_in
        dirfiles = os.listdir(dir_in)
        fullpaths = map(lambda name: os.path.join(dir_in, name), dirfiles)
        dirs = []
        for file in fullpaths:
            if os.path.isdir(file): dirs.append(file)

        # Add dir_in to the dirs list to analyse the files in it
        dirs.append(dir_in) 
        
        # Calculate number of files
        las_files = []
        for dir in dirs:
            
            files = os.listdir(dir)
            # LAS files
            for file in files:
                if file.endswith(extension_in): las_files.append(os.path.join(dir, file))

        # Uptade maximum of the progress bar
        self.progressbar.configure(maximum=len(las_files))
        self.update()

        # Read and write all the files
        for file_in in las_files:
            
            # Check cancel buttom
            if self.cancel_press: self.cancel_press=False ; return

            # Read file
            point_cloud = laspy.read(file_in)

            # Folder and name
            folder_in = file_in.split("/")
            name_in = folder_in[-1]
            folder_in = "/".join(folder_in[:-1])

            # Output folder
            folder_out = folder_in.replace(dir_in, dir_out)
            # Create folder if it does not exist
            if not os.path.isdir(folder_out): os.mkdir(folder_out)

            # Change extension
            name_out = name_in.replace(extension_in, extension_out)

            # Write file
            file_out = os.path.join(folder_out, name_out)
            point_cloud.write(file_out)

            # Delete file
            if delete_files: os.remove(file_in)
            
            # Update bar
            self.progressbar.step(1)
            self.update()
        
        # Finish message
        self.cancel_buttom.configure(state="disable")
        self.start_buttom.configure(state="normal")
        self.information.configure(text="Process finished. Perdón por el retraso ;(")
