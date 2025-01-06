import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

class QueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue Management System")
        
        # Maximize to full screen
        self.root.state('zoomed')  # This maximizes the window to full screen
        self.root.config(bg="#f4f4f4")

        # Creating the Queue
        self.queue = []

        # Title Label with bigger font
        self.title_label = tk.Label(self.root, text="Real Estate Queue Management", font=("Arial", 24, "bold"), bg="#f4f4f4")
        self.title_label.grid(row=0, column=0, columnspan=4, pady=20, padx=20)

        # Username and Phone Number Labels and Entry Fields with larger font size
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 16), bg="#f4f4f4")
        self.username_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.username_entry = tk.Entry(self.root, font=("Arial", 16), width=40, borderwidth=2)
        self.username_entry.grid(row=1, column=1, padx=20, pady=10)

        self.phone_label = tk.Label(self.root, text="Phone Number (078, 079):", font=("Arial", 16), bg="#f4f4f4")
        self.phone_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.phone_entry = tk.Entry(self.root, font=("Arial", 16), width=40, borderwidth=2)
        self.phone_entry.grid(row=2, column=1, padx=20, pady=10)

        # Instructions Label with larger font
        self.instruction_label = tk.Label(self.root, text="Enter Property Details or Client Request:", font=("Arial", 16), bg="#f4f4f4")
        self.instruction_label.grid(row=3, column=0, sticky="w", padx=20, pady=10)

        # Entry Field for Request/Property Info with larger font size
        self.entry = tk.Entry(self.root, font=("Arial", 16), width=40, borderwidth=2)
        self.entry.grid(row=3, column=1, padx=20, pady=10)

        # Buttons to interact with the Queue with bigger font and padding
        self.enqueue_button = tk.Button(self.root, text="Add Request", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", command=self.enqueue)
        self.enqueue_button.grid(row=4, column=0, columnspan=2, pady=15, padx=20, sticky="ew")

        self.dequeue_button = tk.Button(self.root, text="Process Request", font=("Arial", 18, "bold"), bg="#FF5733", fg="white", command=self.dequeue)
        self.dequeue_button.grid(row=5, column=0, columnspan=2, pady=15, padx=20, sticky="ew")

        self.view_button = tk.Button(self.root, text="View Queue", font=("Arial", 18, "bold"), bg="#2196F3", fg="white", command=self.view_queue)
        self.view_button.grid(row=6, column=0, columnspan=2, pady=15, padx=20, sticky="ew")

        # Table to display the Queue (using Treeview) with larger font size
        self.tree = ttk.Treeview(self.root, columns=("Username", "Phone", "Request"), show="headings", height=10)
        self.tree.heading("Username", text="Username")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Request", text="Request")
        self.tree.column("Username", anchor="w", width=200)
        self.tree.column("Phone", anchor="center", width=150)
        self.tree.column("Request", anchor="w", width=300)
        self.tree.grid(row=7, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

        # Configure row and column weights to make the UI responsive
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def validate_phone(self, phone_number):
        """Validate the phone number to check if it's 10 digits and starts with 078 or 079."""
        if re.match(r"^(078|079)\d{7}$", phone_number):
            return True
        else:
            messagebox.showwarning("Invalid Phone", "Phone number must be 10 digits and start with 078 or 079.")
            return False

    def enqueue(self):
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        request = self.entry.get()

        if username and phone and request:
            if self.validate_phone(phone):
                self.queue.append((username, phone, request))
                self.username_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.entry.delete(0, tk.END)
                self.update_output(f"Added to Queue: {request}")
            else:
                self.username_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def dequeue(self):
        if self.queue:
            processed_item = self.queue.pop(0)
            self.update_output(f"Processed: {processed_item[2]}")
        else:
            messagebox.showwarning("Queue Empty", "No requests to process.")

    def view_queue(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if self.queue:
            for item in self.queue:
                self.tree.insert("", "end", values=item)
        else:
            self.update_output("Queue is empty.")

    def update_output(self, text):
        """Displays a message in the output display."""
        messagebox.showinfo("Queue Update", text)

# Circular Queue Class Implementation
class CircularQueueApp(QueueApp):
    def __init__(self, root, size=5):
        super().__init__(root)
        self.size = size
        self.queue = [None] * self.size
        self.front = self.rear = -1

        self.title_label.config(text="Circular Queue Management")

    def enqueue(self):
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        request = self.entry.get()

        if username and phone and request:
            if self.validate_phone(phone):
                if (self.rear + 1) % self.size == self.front:
                    messagebox.showwarning("Queue Full", "Queue is full, cannot add more requests.")
                elif self.front == -1:
                    self.front = self.rear = 0
                    self.queue[self.rear] = (username, phone, request)
                    self.username_entry.delete(0, tk.END)
                    self.phone_entry.delete(0, tk.END)
                    self.entry.delete(0, tk.END)
                    self.update_output(f"Added to Queue: {request}")
                else:
                    self.rear = (self.rear + 1) % self.size
                    self.queue[self.rear] = (username, phone, request)
                    self.username_entry.delete(0, tk.END)
                    self.phone_entry.delete(0, tk.END)
                    self.entry.delete(0, tk.END)
                    self.update_output(f"Added to Queue: {request}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def dequeue(self):
        if self.front == -1:
            messagebox.showwarning("Queue Empty", "No requests to process.")
        elif self.front == self.rear:
            processed_item = self.queue[self.front]
            self.front = self.rear = -1
            self.update_output(f"Processed: {processed_item[2]}")
        else:
            processed_item = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            self.update_output(f"Processed: {processed_item[2]}")

    def view_queue(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if self.front != -1:
            i = self.front
            while i != self.rear:
                self.tree.insert("", "end", values=self.queue[i])
                i = (i + 1) % self.size
            self.tree.insert("", "end", values=self.queue[self.rear])
        else:
            self.update_output("Queue is empty.")

# Main Program to Run the Queue Management System
def run_queue_app():
    root = tk.Tk()
    app = CircularQueueApp(root)  # To use Circular Queue, change this to QueueApp for normal Queue
    root.mainloop()

if __name__ == "__main__":
    run_queue_app()
