import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.filedialog as fd
import os
import tkVideoPlayer as tkv
import subprocess
import threading
import PerformanceDetection_GUI
import queue
import shared_data

output_file_name = "output" 

input_filepath = None
output_filepath = None

def update_results():
    try:
        while not PerformanceDetection_GUI.counter1_queue.empty():
            counter1 = PerformanceDetection_GUI.counter1_queue.get_nowait()
            staff1_value.set(counter1)

        while not PerformanceDetection_GUI.counter2_queue.empty():
            counter2 = PerformanceDetection_GUI.counter2_queue.get_nowait()
            staff2_value.set(counter2)

    except queue.Empty:
        pass

    app.after(100, update_results)

def execute_analysis():
    if not input_filepath:
        print("No input video selected.")
        return
    #PerformanceDetection_GUI.run_analysis(input_filepath, output_file_name, check_person, check_arcup, check_cup, check_preview, app)
    app.after(100)
    app.update()
    analysis_thread = threading.Thread(target=PerformanceDetection_GUI.run_analysis, args=(input_filepath, output_file_name, check_person, check_arcup, check_cup, check_preview))
    analysis_thread.start() 
    # execute_frame.after(0, update_results)
    # execute_frame.update_idletasks()

def select_input_file():
    global input_filepath
    filetypes = (("MP4 files", "*.mp4"), ("All files", "*.*"))
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_folder = os.path.join(script_dir, "Input")
    if not os.path.isdir(input_folder): #Error Handling for if Input folder does not exist under root/Input
        print(f"Error: Input folder '{input_folder}' not found.")
        return  # Don't open the dialog if the folder doesn't exist
    filepath = fd.askopenfilename(title="Open Input Video", initialdir=input_folder, filetypes=filetypes)

    if filepath:
        input_filepath = filepath
        filename = os.path.basename(filepath)
        filename_entry.configure(state="normal")
        filename_entry.delete(0, "end")
        filename_entry.insert(0, filename)
        filename_entry.configure(state="readonly")

        print(f"Selected input file: {filepath}")

def select_output_file():
    global output_filepath
    filetypes = (("MP4 files", "*.mp4"), ("All files", "*.*"))
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_folder = os.path.join(script_dir, "Output")
    if not os.path.isdir(output_folder): #Error Handling for if Output folder does not exist under root/Input
        print(f"Error: Output folder '{output_folder}' not found.")
        return  # Don't open the dialog if the folder doesn't exist
    filepath = fd.askopenfilename(title="Open Output Video", initialdir=output_folder, filetypes=filetypes)

    if filepath:
        output_filepath = filepath
        filename = os.path.basename(filepath)
        output_filename_entry.configure(state="normal")
        output_filename_entry.delete(0, "end")
        output_filename_entry.insert(0, filename)
        output_filename_entry.configure(state="readonly")

        print(f"Selected output file: {filepath}")

def update_output_name(*args):
    global output_file_name
    output_file_name = output_entry.get()
    print(f"Output file name updated: {output_file_name}")

# def select_file():
#     filetypes = (("MP4 files", "*.mp4"), ("All files", "*.*"))
#     filepath = fd.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)

#     if filepath:
#         filename = os.path.basename(filepath)
#         filename_entry.configure(state="normal")
#         filename_entry.delete(0, "end")
#         filename_entry.insert(0, filename)
#         filename_entry.configure(state="readonly")

#         # Call your project function here, passing 'filepath' as an argument
#         print(f"Selected file: {filepath}")

def play_video():
    if output_filepath:  # Play the output video (if selected)
        videoplayer = tkv.TkinterVideo(master=preview_frame, scaled=True)
        videoplayer.load(output_filepath)
        # Set desired video player dimensions
        desired_width = 720
        desired_height = int(desired_width*9/16)
        videoplayer.configure(width=desired_width, height=desired_height)
        # Place the video player
        videoplayer.grid(row=3, column=0, rowspan=9, columnspan=6, pady=10, padx=10, sticky = 'nsew')
        # Configure row and column to expand to the video player's size
        preview_frame.rowconfigure(3, weight=1)  # Expand row to video height
        preview_frame.columnconfigure(0, weight=1)  # Expand column to video width
        videoplayer.play()
    else:
        print("No output video selected.")

def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"+{x}+{y}")


app = ttk.Window(themename="darkly")  
app.title("Café Analyzer")
app.geometry("800x600")
#initializing Staff1 and Staff2 variables right after app initialization
staff1_value = tk.StringVar(value="0")
staff2_value = tk.StringVar(value="0")

# Create a Notebook widget to hold the tabs
notebook = ttk.Notebook(app)
notebook.grid(row=0, column=0, sticky="nsew")  # Place notebook in the grid
app.rowconfigure(0, weight=1)  # Allow row to expand
app.columnconfigure(0, weight=1)  # Allow column to expand
# Create the "Configure" tab
configure_frame = ttk.Frame(notebook)
notebook.add(configure_frame, text="Configure")
# Create the "Preview" tab
preview_frame = ttk.Frame(notebook)
notebook.add(preview_frame, text="Preview")
# Create the "stats" tab
execute_frame = ttk.Frame(notebook)
notebook.add(execute_frame, text="Execute & Analysis") #can use notebook. Insert instead to positionally lock which tab appears first


# Welcome Label
welcome_label = ttk.Label(configure_frame, text="Welcome to Employee Performance Tracker")
welcome_label.grid(row=1, column=0, columnspan=2, pady=(20, 10))  # Span 2 columns

labelframe_files = ttk.Labelframe(configure_frame, text="File Settings")
labelframe_files.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
# Configure Tab - Select MP4 Label
input_mp4_label = ttk.Label(labelframe_files, text="Select the input MP4 file:")
input_mp4_label.grid(row=2, column=0, pady=(10, 0), sticky="w")  # Align to the left
# File name entry
filename_entry = ttk.Entry(labelframe_files, state="readonly")  
filename_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")  # Expand to fill width
# Browse button
button = ttk.Button(labelframe_files, text="Browse", command=select_input_file)  
button.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="e")  # Align to the right

# Configure Tab - Output File Name Label
output_label = ttk.Label(labelframe_files, text="Output File Name:")
output_label.grid(row=4, column=0, pady=(10, 0), sticky="w")
# Output File Name Entry
output_entry = ttk.Entry(labelframe_files)
output_entry.insert(0, output_file_name)  # Set default text
output_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=(10,0), sticky="ew")
output_entry.bind("<Return>", update_output_name)  # Update on Enter key press
output_entry.bind("<FocusOut>", update_output_name)  # Update on losing focus

labelframe_opt = ttk.Labelframe(configure_frame, text="Togglable Options")
labelframe_opt.grid(row=6, column=0, padx=20, pady=20, sticky="nsew")
# configure_frame.columnconfigure(6, weight=1)
# configure_frame.rowconfigure(6, weight=1)
check_person = tk.IntVar()
check_cup = tk.IntVar()
check_arcup = tk.IntVar() #Ex: use check_person.get() to get the value of the checkbox.
check_preview = tk.IntVar()
ttk.Checkbutton(labelframe_opt, text="Enable Person Tracking", variable=check_person).grid(row=7, column=0, pady=6, sticky="w")
ttk.Checkbutton(labelframe_opt, text="Enable Cup Tracking", variable=check_cup).grid(row=8, column=0, pady=6,sticky="w")
ttk.Checkbutton(labelframe_opt, text="Enable Cup Registration Area", variable=check_arcup).grid(row=9, column=0, pady=6, sticky="w")
ttk.Checkbutton(labelframe_opt, text="Enable Live Preview", variable=check_preview).grid(row=10, column=0, pady=6, sticky="w")


# Preview Tab - Output Video + Play button
output_mp4_label = ttk.Label(preview_frame, text="Select an output video to play!")
output_mp4_label.grid(row=1, column=0, pady=(20, 0), sticky="w")  # Align to the left
output_button = ttk.Button(preview_frame, text="Browse Output", command=select_output_file)
output_button.grid(row=1, column=2, padx=5, pady=(20, 0), sticky="e")
output_filename_entry = ttk.Entry(preview_frame, state="readonly")
output_filename_entry.grid(row=1, column=1, padx=5, pady=(20, 0), sticky="ew")
play_button = ttk.Button(preview_frame, text="Play Video", command=play_video, bootstyle=SUCCESS)
play_button.grid(row=2, column=0, columnspan=2, pady=10)


# Execution Tab
execute_message = ttk.Label(execute_frame, text="Please ensure you have selected the right configuration before proceeding")
execute_message.grid(row=3, column=0, pady=10, sticky='w')
labelframe_analysis = ttk.Labelframe(execute_frame, text="Analytical Statistics")
labelframe_analysis.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

staff1_stat = ttk.Label(labelframe_analysis, text="Cups served by Staff 1")
staff1_stat.grid(row=4, column=0, pady=6, sticky='w')
staff1_entry = ttk.Entry(labelframe_analysis, state="readonly", textvariable=staff1_value)  # Create the entry first
staff1_entry.grid(row=4, column=1, padx=5, pady=6, sticky="ew")  # Then place it in the grid
staff1_entry.insert(0, "0") #initializing with 0
staff2_stat = ttk.Label(labelframe_analysis, text="Cups served by Staff 2")
staff2_stat.grid(row=5, column=0, pady=6, sticky='w')
staff2_entry = ttk.Entry(labelframe_analysis, state="readonly", textvariable=staff2_value)  # Create the entry first
staff2_entry.grid(row=5, column=1, padx=5, pady=6, sticky="ew")  # Then place it in the grid
staff2_entry.insert(0, "0") #initializing with 0
execute_button = ttk.Button(execute_frame, text="Run Cafe Analysis", command=execute_analysis, bootstyle=SUCCESS) #Add command here to run the main script 
execute_button.grid(row=10, column=0, columnspan = 2, padx=(50,0), pady=10)

app.after(100, lambda: center_window(app))
app.after(100, update_results)
app.mainloop()
