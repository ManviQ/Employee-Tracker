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
import GenAI

output_file_name = "output" 
staff1_n = "Staff 1"
staff2_n = "Staff 2"

input_filepath = None
output_filepath = None

def start_genai_chatbox():
    chat_window = tk.Toplevel()  # Create a new window for the chatbox
    chat_window.title("Gemini AI Chat")  # Set the title
    chat_window.geometry("600x500")  # Set the dimensions

    # Create a text widget for displaying the conversation
    chat_text = tk.Text(chat_window, wrap="word")
    chat_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Create a scrollbar for the text widget
    scrollbar = tk.Scrollbar(chat_window, command=chat_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    chat_text.config(yscrollcommand=scrollbar.set)

    # Create an entry widget for user input
    entry_field = tk.Entry(chat_window)
    entry_field.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    def send_message():
        user_input = entry_field.get()
        if user_input:
            # Display user's message in the chat window
            chat_text.insert(tk.END, f"You: {user_input}\n")
            chat_text.see(tk.END)  # Scroll to the end
            entry_field.delete(0, tk.END)  # Clear the entry field

            # Pass user input to the function that interacts with Gemini AI
            response = interact_with_gemini(user_input)

            # Display Gemini's response in the chat window
            chat_text.insert(tk.END, f"Gemini AI: {response}\n")
            chat_text.see(tk.END)  # Scroll to the end

    # Function to interact with Gemini AI based on user input
    def interact_with_gemini(user_input):
    #     # Call the function to interact with Gemini AI from GenAI module
        return user_input

    # Create a button for sending messages
    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.grid(row=1, column=1, padx=5, pady=5)

    # Bind the Enter key to the send_message function
    chat_window.bind("<Return>", lambda event: send_message())

# Function to execute GenAI conversation in a thread




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
    analysis_thread = threading.Thread(target=PerformanceDetection_GUI.run_analysis, args=(input_filepath, output_file_name, check_person, check_arcup, check_cup, check_preview, staff1_n, staff2_n))
    analysis_thread.start() 
    # execute_frame.after(0, update_results)
    # execute_frame.update_idletasks()

def execute_genai():
    if not output_filepath:
        print("No output video selected.")
        return

    # Start a new thread for the GenAI conversation
    genai_thread = threading.Thread(target=GenAI.have_conversation_with_gemini, args=(output_filepath,))
    genai_thread.start()
    start_genai_chatbox()


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

def update_staff1_name(*args):
    global staff1_n
    staff1_n = staff1_nentry.get()
    print(f"Staff 1 name has been updated: {staff1_n}")
    staff1_stat.config(text=f"Cups served by {staff1_n}")

def update_staff2_name(*args):
    global staff2_n
    staff2_n = staff2_nentry.get()
    print(f"Staff 2 name has been updated: {staff2_n}")
    staff2_stat.config(text=f"Cups served by {staff2_n}")

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
# Create the "Experimental" tab
experiment_frame = ttk.Frame(notebook)
notebook.add(experiment_frame, text="Experimental - GenAI")


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

# Configure Tab - Customizations Container
labelframe_custom = ttk.Labelframe(configure_frame, text="Customizations")
labelframe_custom.grid(row=6, column=2, padx=20, pady=20, sticky="nsew")

#Customizations Container - staff 1 Name label
staff1_label = ttk.Label(labelframe_custom, text="Set name for Staff 1: ")
staff1_label.grid(row=7, column=2, pady=(10, 0), sticky="w")
# Staff 1 Name Entry
staff1_nentry = ttk.Entry(labelframe_custom)
staff1_nentry.insert(0, staff1_n)  # Set default text
staff1_nentry.grid(row=7, column=3, columnspan=2, padx=5, pady=(10,0), sticky="ew")
staff1_nentry.bind("<Return>", update_staff1_name)  # Update on Enter key press
staff1_nentry.bind("<FocusOut>", update_staff1_name)  # Update on losing focus

# Customizations Container - Staff 2 Name Label
staff2_label = ttk.Label(labelframe_custom, text="Set name for Staff 2: ")
staff2_label.grid(row=8, column=2, pady=(10, 0), sticky="w")
# Staff 2 Name Entry
staff2_nentry = ttk.Entry(labelframe_custom)
staff2_nentry.insert(0, staff2_n)  # Set default text
staff2_nentry.grid(row=8, column=3, columnspan=2, padx=5, pady=(10,0), sticky="ew")
staff2_nentry.bind("<Return>", update_staff2_name)  # Update on Enter key press
staff2_nentry.bind("<FocusOut>", update_staff2_name)  # Update on losing focus


# Preview Tab - Output Video + Play button
welcome_label = ttk.Label(preview_frame, text="If you have a processed output, select the output file and play them here!")
welcome_label.grid(row=1, column=0, columnspan=2, pady=(20, 10))  # Span 2 columns
output_mp4_label = ttk.Label(preview_frame, text="Select an output video to play!")
output_mp4_label.grid(row=2, column=0, pady=(20, 0), sticky="w")  # Align to the left
output_button = ttk.Button(preview_frame, text="Browse Output", command=select_output_file)
output_button.grid(row=2, column=2, padx=5, pady=(20, 0), sticky="e")
output_filename_entry = ttk.Entry(preview_frame, state="readonly")
output_filename_entry.grid(row=2, column=1, padx=5, pady=(20, 0), sticky="ew")
play_button = ttk.Button(preview_frame, text="Play Video", command=play_video, bootstyle=SUCCESS)
play_button.grid(row=3, column=0, columnspan=2, pady=10)


# Execution Tab
execute_message = ttk.Label(execute_frame, text="Please ensure you have selected the right configuration before proceeding")
execute_message.grid(row=3, column=0, pady=10, sticky='w')
labelframe_analysis = ttk.Labelframe(execute_frame, text="Analytical Statistics")
labelframe_analysis.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

staff1_stat = ttk.Label(labelframe_analysis, text=f"Cups served by {staff1_n}")
staff1_stat.grid(row=4, column=0, pady=6, sticky='w')
staff1_entry = ttk.Entry(labelframe_analysis, state="readonly", textvariable=staff1_value)  # Create the entry first
staff1_entry.grid(row=4, column=1, padx=5, pady=6, sticky="ew")  # Then place it in the grid
staff1_entry.insert(0, "0") #initializing with 0
staff2_stat = ttk.Label(labelframe_analysis, text=f"Cups served by {staff2_n}")
staff2_stat.grid(row=5, column=0, pady=6, sticky='w')
staff2_entry = ttk.Entry(labelframe_analysis, state="readonly", textvariable=staff2_value)  # Create the entry first
staff2_entry.grid(row=5, column=1, padx=5, pady=6, sticky="ew")  # Then place it in the grid
staff2_entry.insert(0, "0") #initializing with 0
execute_button = ttk.Button(execute_frame, text="Run Cafe Analysis", command=execute_analysis, bootstyle=SUCCESS) #Add command here to run the main script 
execute_button.grid(row=10, column=0, columnspan = 2, padx=(50,0), pady=10)

# Experimental Tab
landing_label = ttk.Label(experiment_frame, text="This is the Experimental Tab where if everything works normally \nAllowing you to have an interaction with an AI and have conversations regarding the output video!")
landing_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))  # Span 2 columns
labelframe_exp = ttk.Labelframe(experiment_frame)
labelframe_exp.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
# Experimental Tab - Select MP4 Label
genai_output_mp4_label = ttk.Label(labelframe_exp, text="Select a processed output file:")
genai_output_mp4_label.grid(row=1, column=0, pady=(10, 0), sticky="w")  # Align to the left
output_button = ttk.Button(labelframe_exp, text="Browse Output", command=select_output_file)
output_button.grid(row=2, column=2, padx=5, pady=(20, 0), sticky="e")
output_filename_entry = ttk.Entry(labelframe_exp, state="readonly")
output_filename_entry.grid(row=2, column=1, padx=5, pady=(20, 0), sticky="ew")
play_button = ttk.Button(labelframe_exp, text="Play Video in preview - WIP", command=play_video, bootstyle=SUCCESS)
play_button.grid(row=3, column=0, columnspan=2, pady=10)
genai_button = ttk.Button(labelframe_exp, text="Converse with Gemini", command=execute_genai, bootstyle=SUCCESS) #Add command here to run the main script 
genai_button.grid(row=4, column=0, columnspan = 2, padx=(50,0), pady=10)



app.after(100, lambda: center_window(app))
app.after(100, update_results)
app.mainloop()
