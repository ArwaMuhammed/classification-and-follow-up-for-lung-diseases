from main import *
from Patient import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class User_interface(ttk.Frame):
    def __init__(self, master, current_patient):
        super().__init__(master)
        self.current_patient = current_patient
        self.image_on_canvas = None

        # Main frame
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill='both', expand=True)

        # Top frame with back button and centered greeting
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.back_button = ttk.Button(self.top_frame, text='Back', width=10, command=self.go_back)
        self.back_button.pack(side='left', padx=5)

        self.text = ttk.Label(
            self.top_frame,
            text=f'Hello, {self.current_patient.name}',
            font=("Arial", 16, "bold"),
            foreground="white",
            background="#42A5F5",
            anchor=tk.CENTER,
            padding=10
        )
        self.text.pack(side='left', fill='x', expand=True, padx=10)

        # Image frame
        self.image_frame = ttk.LabelFrame(self.main_frame, text="Uploaded Image", padding=10)
        self.image_frame.config(borderwidth=2, relief="solid")
        self.image_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(
            self.image_frame, width=500, height=500,
            bg="#E3F2FD", highlightthickness=1, highlightbackground="gray"
        )
        self.canvas.pack(pady=10)

        self.upload_button = ttk.Button(self.image_frame, text='Upload Image', width=15, command=self.upload_image)
        self.upload_button.pack(pady=5)

        # Graph frame
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Patient Progression", padding=10)
        self.graph_frame.config(borderwidth=2, relief="solid")
        self.graph_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Initialize Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(figsize=(6, 6))  # Larger figure size
        self.ax.set_facecolor("#F8F9FA")  # Light background for the plot
        self.ax.set_title("Diagnosis", fontsize=16, pad=40)  # Lowered title with increased padding
        self.canvas_graph = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas_graph.get_tk_widget().pack(fill='both', expand=True)

        # Configure consistent sizing
        self.main_frame.columnconfigure(0, weight=1, uniform="same_size")
        self.main_frame.columnconfigure(1, weight=1, uniform="same_size")
        self.main_frame.rowconfigure(1, weight=1)

        self.plot_progression()


    def upload_image(self):
       # Open file dialog to choose an image
       file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

       if file_path:
          self.image_path = file_path

          # Open the image using Pillow
          image = Image.open(file_path)

          # Get the current size of the canvas
          canvas_width = self.canvas.winfo_width()
          canvas_height = self.canvas.winfo_height()

          # Calculate the aspect ratio of the image
          aspect_ratio = image.width / image.height

          # Calculate the new dimensions based on the canvas size
          if canvas_width / aspect_ratio <= canvas_height:
            new_width = canvas_width
            new_height = int(canvas_width / aspect_ratio)
          else:
            new_height = canvas_height
            new_width = int(canvas_height * aspect_ratio)

          # Resize the image to fit the canvas while maintaining the aspect ratio
          image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

          # Convert the image to a format Tkinter can use
          image = ImageTk.PhotoImage(image)

          # If there is already an image, remove it from the canvas
          if self.image_on_canvas:
            self.canvas.delete(self.image_on_canvas)

          # Place the resized image onto the canvas (centered)
          self.image_on_canvas = self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=image)

          # Keep a reference to the image to avoid garbage collection
          self.canvas.image = image

          self.enter()

    def enter(self):
        #integrate with model
        dict = System.connect_to_model(self.image_path)

        #new user
        if self.current_patient.diagnosis == None or self.current_patient.diagnosis == 'Normal':
            max_diagnosis = max(dict, key=dict.get)
            max_value = dict[max_diagnosis]
            diagnosis = max_diagnosis if max_value >= 0.3 else 'Normal'
            progression = dict[max_diagnosis]
            self.current_patient.add_diagnosis(diagnosis)
            self.current_patient.add_progression(progression)

        #old user
        else:
            progression = dict[self.current_patient.diagnosis]
            self.current_patient.add_progression(progression)

        self.plot_progression()

    def plot_progression(self):
    # Assuming current_patient.progressions contains updated values
        progressions = self.current_patient.progressions

        if not progressions:  # Check if progressions is empty
           self.ax.clear()
           self.ax.set_title("No progression data available", fontsize=14, pad=20)
           self.canvas_graph.draw()
           return

        time = list(range(1, len(progressions) + 1))

        self.ax.clear()  # Clear previous plot
        self.ax.plot(time, progressions, marker='o', linestyle='-', color='b', label="Progression Over Time")
        self.ax.set_xlim(0.8, max(5, len(time) + 1))   # Adjust x-axis dynamically
        self.ax.set_ylim(0, 1.1)  # Adjust y-axis to suit the range
        self.ax.set_title("diagnosis: "+str(self.current_patient.diagnosis), fontsize=14, pad=20)  # Set title at the top of the graph
        self.ax.set_xlabel("Time", fontsize=12, labelpad=10) # Place label for x-axis
        self.ax.set_ylabel("Progression", fontsize=12, labelpad=10)

        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        # Remove all numbers on both axes
        self.ax.set_xticks(range(1, max(5, len(time) + 1)))  # Set x-axis ticks dynamically
        self.ax.set_yticks([i / 10 for i in range(0, 12)]) # Remove numbers on the y-axis

        self.ax.tick_params(axis='both', which='both', labelbottom=False, labelleft=False)

        # Display the legend
        self.ax.legend(loc="lower right")

        # Redraw the canvas to reflect changes
        self.canvas_graph.draw()
    def go_back(self):
        self.destroy()
        self.master.create_widgets()