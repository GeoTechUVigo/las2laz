from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import *
from pathlib import Path
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
        self.information_input = ttk.Label(text="", wraplength="100m") # Limit the maximum width

        # Output dir
        self.label_out_dir = ttk.Label(text="Output dir: ")
        self.button_out_dir = ttk.Button(text='Select', command=self.select_dir_out)
        self.information_output = ttk.Label(text="", wraplength="100m") # Limit the maximum width

        # Save in the same dir button
        self.label_same_dir = ttk.Label( text="Save in the same dir")
        self.same_dir = BooleanVar()
        self.buttom_same_dir = ttk.Checkbutton(variable=self.same_dir, onvalue=True, offvalue=False, command=self.same_dir_func)

        # Analyse subdirs button
        self.label_subdirs = ttk.Label( text="Analyse files in subdirs")
        self.analyse_subdirs = BooleanVar()
        self.buttom_analyse_subdirs = ttk.Checkbutton(variable=self.analyse_subdirs, onvalue=True, offvalue=False)


        # Delete original files button
        self.label_delete_files = ttk.Label( text="Delete original files")
        self.delete_files = BooleanVar()
        self.butoom_delete_files = ttk.Checkbutton(variable=self.delete_files, onvalue=True, offvalue=False)

        # Start process
        self.start_buttom = ttk.Button(text="Start", command=self.start_process)
        
        # Cancel process 
        self.cancel = BooleanVar()
        self.cancel_buttom = ttk.Button(text="Cancel", state='disable', command=self.cancel_process)

        # Information
        self.information = ttk.Label(text="")

        # Progress bar
        self.progressbar = ttk.Progressbar(self, orient='horizontal', value=0, maximum=100, mode='determinate')

        # Define the geometry of the content in the GUI
        self.label_in_dir.grid(column=1, row=1, sticky="nsew")
        self.button_in_dir.grid(column=2, row=1, sticky="nsew")
        self.information_input.grid(column=3, row=1, sticky="nsew")
        self.label_out_dir.grid(column=1, row=2, sticky="nsew")
        self.button_out_dir.grid(column=2, row=2, sticky="nsew")
        self.information_output.grid(column=3, row=2, sticky="nsew")
        self.label_same_dir.grid(column=1, row=3, sticky="nsew")
        self.buttom_same_dir.grid(column=2, row=3, sticky="nsew")
        self.label_subdirs.grid(column=1, row=4, sticky="nsew")
        self.buttom_analyse_subdirs.grid(column=2, row=4, sticky="nsew")
        self.label_delete_files.grid(column=1, row=5, sticky="nsew")
        self.butoom_delete_files.grid(column=2, row=5, sticky="nsew")
        self.start_buttom.grid(column=3, row=7, sticky="nsew")
        self.cancel_buttom.grid(column=4, row=7, sticky="nsew")
        self.progressbar.grid(column=1, row=7, sticky="nsew")
        self.information.grid(column=1, row=8, sticky="nsew")

        # This is done to have padding around all widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=2)


    def select_dir_in(self):
        self.dir_in = fd.askdirectory(title='Select directory', initialdir='./', mustexist=True)
        self.information_input.configure(text=self.dir_in[-60:])


    def select_dir_out(self):
        self.dir_out = fd.askdirectory(title='Select directory', initialdir='./', mustexist=True)
        self.information_output.configure(text=self.dir_out)


    def same_dir_func(self):
        if self.same_dir.get() == True:
            self.button_out_dir["state"] = "disable"
            self.information_output.configure(text=self.dir_in)
        else:
            self.button_out_dir["state"] = "normal"
            self.information_output.configure(text=self.dir_out)


    def start_process(self):

        # Correct dir_out
        if self.same_dir.get() == True:
            self.dir_out = self.dir_in

        # Check inputs
        if not Path(self.dir_in).is_dir():
            self.information.configure(text="Incorrect dir in")


        elif not Path(self.dir_out).is_dir():
            self.information.configure(text="Incorrect dir out")

        # Start process
        else:
            # Updating start and cancel buttoms
            self.start_buttom.configure(state="disable")
            self.cancel_buttom.configure(state="normal")
            self.information.configure(text="Working")
            self.update()
            self.las2laz()


    def cancel_process(self):
        self.cancel_press = True
        self.cancel_buttom.configure(state="disable")
        self.start_buttom.configure(state="normal")
        self.information.configure(text="Canceled")
    

    def las2laz(self):
        
        dir_in = Path(self.dir_in)
        dir_out = Path(self.dir_out)
        delete_files = self.delete_files.get()

        # Extension in and out
        suffix_in = '.las'
        suffix_out = '.laz'

        # List with the subdirs, the LAS files in the principal dir and the output file names. Create subdir in dir_out
        # fullpaths = map(lambda name: os.path.join(dir_in, name), dirfiles)
        subdirs = list()
        las_files = list()
        laz_files = list()
        for file in dir_in.iterdir():
            if file.is_dir(): 
                subdirs.append(file.name)

            elif file.suffix == suffix_in: 
                las_files.append(file)
                laz_files.append(dir_out.joinpath(file.stem + suffix_out)) # Change suffix
        
        # Add to las_files_in and out the las files in the subdirs 
        if self.analyse_subdirs.get():

            for subdir_name in subdirs:

                # Create this folder in dir_out
                subdir_path = dir_out.joinpath(subdir_name)
                subdir_path.mkdir(exist_ok=True)

                # Files in this subdir
                subdir = dir_in.joinpath(subdir_name)
                for file in subdir.iterdir():
                    if file.suffix == suffix_in:
                        las_files.append(file)
                        laz_files.append(dir_out.joinpath(subdir_name, file.stem + suffix_out))

        # Uptade maximum of the progress bar
        self.progressbar.configure(maximum=len(las_files))
        self.progressbar.configure(value=0)
        self.update()

        # Read and write all the files
        for file_in, file_out in zip(las_files, laz_files):

            # Check cancel buttom
            if self.cancel_press: self.cancel_press = False; return

            # Read file
            point_cloud = laspy.read(file_in)

            # Write file
            point_cloud.write(file_out)

            # Delete file
            if delete_files: file_in.unlink()
            
            # Update bar
            self.progressbar.step(1)
            self.update()
        
        # Finish message
        self.cancel_buttom.configure(state="disable")
        self.start_buttom.configure(state="normal")
        self.information.configure(text="Process finished. Perdón por el retraso ;(")
