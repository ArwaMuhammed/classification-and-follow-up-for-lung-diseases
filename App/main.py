import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import csv
from Patient import Patient
from System import System

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Import data from CSV
        with open('memory.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                progressions = list(map(float, row["Progressions"].split(';'))) if row["Progressions"] else []
                patient = Patient(row["Name"], row["ID"], row["Diagnosis"], progressions)
                System.patients.append(patient)

        self.title('Track Your Health')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        icon = PhotoImage(file="2nd.png")
        self.iconphoto(True, icon)

        self.create_widgets()
        self.user_is_being_created = False

    def on_exit(self):
        # Save data to CSV
        with open('memory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID", "Diagnosis", "Progressions"])
            for patient in System.patients:
                progressions_str = ';'.join(map(str, patient.progressions))
                writer.writerow([patient.name, patient.ID, patient.diagnosis, progressions_str])

        self.destroy()

    def create_widgets(self):
        # Main frame with padding
        self.main_frame = tk.Frame(self, bg='#E3F2FD')
        self.main_frame.pack(fill='both', expand=True)

        img = PhotoImage(file="2nd.png")
        img_label = tk.Label(self.main_frame, image=img, bg='#E3F2FD')
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.place(y=100, x=600, anchor="nw")

        # Search frame
        self.search_frame = tk.Frame(self.main_frame, bg='#E3F2FD')
        self.search_frame.place(y=200, x=300, anchor="nw")

        # Label with frame
        self.label_frame = tk.Frame(
            self.search_frame,
            background="#BBDEFB",
            highlightbackground="#1976D2",
            highlightthickness=2
        )
        self.label_frame.pack(pady=10)

        self.text = ttk.Label(
            self.label_frame,
            text='Enter your ID',
            font=("Arial", 14, "bold"),
            anchor=tk.CENTER,
            padding=10
        )
        self.text.pack()

        self.searched_ID = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.searched_ID,
            font=("Arial", 15),
            width=20,
            bd=2,
            relief="solid"
        )
        self.search_entry.pack(pady=10)

        self.search_button = ttk.Button(
            self.search_frame,
            text='Search',
            width=20,
            command=self.search,
            style="RoundedButton.TButton"
        )
        self.search_button.pack(side='bottom', pady=10)

        self.search_error_var = tk.StringVar()
        self.error_text = tk.Label(self.search_frame, textvariable=self.search_error_var, fg='red', bg='#E3F2FD')

        # Create new user frame
        self.create_frame = tk.Frame(self.main_frame, bg='#E3F2FD')
        self.create_frame.place(y=200, x=self.screen_width-300, anchor="ne")

        self.new_ID = tk.StringVar()
        self.new_ID_text = tk.Label(
            self.create_frame,
            textvariable=self.new_ID,
            fg='blue',
            font=("Arial", 14, "bold")
        )

        self.create_label_frame = tk.Frame(
            self.create_frame,
            background="#C8E6C9",
            highlightbackground="#388E3C",
            highlightthickness=2
        )
        self.create_label_frame.pack(pady=10)

        self.text = ttk.Label(
            self.create_label_frame,
            text="Don't have an ID?",
            font=("Arial", 14),
            anchor=tk.CENTER,
            padding=10
        )
        self.text.pack()

        self.create_button = ttk.Button(
            self.create_frame,
            text='Create a New User',
            width=20,
            command=self.create_user,
            style="RoundedButton.TButton"
        )
        self.create_button.pack(pady=10)

        # Configure button styles for rounded appearance
        self.style = ttk.Style()
        self.style.configure(
            "RoundedButton.TButton",
            font=("Arial", 12),
            padding=10,
            relief="flat",  # No border for flat look
            background="#4CAF50",
            foreground="black",
            borderwidth=2,
            anchor="center"
        )
        self.style.map(
            "RoundedButton.TButton",
            background=[("active", "#388E3C")],
            foreground=[("active", "dark blue")],
            relief=[("pressed", "sunken"), ("!pressed", "raised")],
        )

    def search(self):
        if self.searched_ID.get() == '':
            pass
        else:
            patient = System.search_patient(self.searched_ID.get())
            if patient == None:
                self.search_error_var.set('Patient is not found')
                self.error_text.pack()
            else:
                from User_interface import User_interface
                self.main_frame.destroy()
                next_scene = User_interface(self, patient)
                next_scene.pack(fill='both', expand=True)

    def create_user(self):
        self.new_ID_text.destroy()
        if not self.user_is_being_created:
            self.create_frame_child1 = tk.Frame(self.create_frame, bg='#E3F2FD')
            self.create_frame_child1.pack(side='bottom', pady=20)

            self.name_label_frame = tk.Frame(
                self.create_frame_child1,
                background="#BBDEFB",
                highlightbackground="#1976D2",
                highlightthickness=2
            )
            self.name_label_frame.pack(pady=10)

            self.text = ttk.Label(
                self.name_label_frame,
                text='Enter your name',
                font=("Arial", 14, "bold"),
                anchor=tk.CENTER,
                padding=10
            )
            self.text.pack()

            self.name = tk.StringVar()
            self.create_entry = tk.Entry(
                self.create_frame_child1,
                textvariable=self.name,
                font=("Arial", 15),
                width=20,
                bd=2,
                relief="solid"
            )
            self.create_entry.pack()

            self.create_button = ttk.Button(
                self.create_frame_child1,
                text='Create',
                width=20,
                command=self.create,
                style="RoundedButton.TButton"
            )
            self.create_button.pack(side='bottom', pady=10)
            self.user_is_being_created = True

    def create(self):
        if self.name.get() == '':
            pass
        else:
            self.user_is_being_created = False
            if hasattr(self, 'new_ID_text') and self.new_ID_text:
                self.new_ID_text.destroy()
            self.create_frame_child1.destroy()
            self.new_ID = tk.StringVar()
            self.new_ID_text = tk.Label(
                self.create_frame,
                textvariable=self.new_ID,
                fg='blue',
                font=("Arial", 14, "bold"),
                bg='#E3F2FD'
            )
            self.new_ID.set("Your ID is: " + str(System.add_patient(self.name.get())))
            self.new_ID_text.pack(side='top', pady=10)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()