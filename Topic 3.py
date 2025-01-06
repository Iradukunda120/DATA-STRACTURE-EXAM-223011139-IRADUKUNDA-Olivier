import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Property Management (Queue-Based)")
        self.root.configure(bg="#F8F9FA")
        
        # Maximize the window
        self.root.state("zoomed")  # For Windows

        # Data Structure
        self.inquiry_queue = deque()  # Queue to manage inquiries

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Fonts
        title_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Add Inquiry", font=title_font, bg="#E9ECEF")
        input_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(input_frame, text="Name:", font=label_font, bg="#E9ECEF").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Phone Number:", font=label_font, bg="#E9ECEF").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(input_frame)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Property Details:", font=label_font, bg="#E9ECEF").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.property_entry = ttk.Entry(input_frame)
        self.property_entry.grid(row=2, column=1, padx=10, pady=5)

        add_button = tk.Button(input_frame, text="Add Inquiry", font=button_font, bg="#28A745", fg="white", command=self.add_inquiry)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Inquiry Table Frame
        table_frame = tk.LabelFrame(self.root, text="Inquiry List", font=title_font, bg="#E9ECEF")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.inquiry_table = ttk.Treeview(table_frame, columns=("Name", "Phone", "Property"), show="headings", height=15)
        self.inquiry_table.heading("Name", text="Name")
        self.inquiry_table.heading("Phone", text="Phone Number")
        self.inquiry_table.heading("Property", text="Property Details")

        self.inquiry_table.column("Name", width=200, anchor="center")
        self.inquiry_table.column("Phone", width=150, anchor="center")
        self.inquiry_table.column("Property", width=300, anchor="center")
        self.inquiry_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Action Buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=20, pady=10)

        process_button = tk.Button(action_frame, text="Process Inquiry", font=button_font, bg="#007BFF", fg="white", command=self.process_inquiry)
        process_button.pack(side="left", padx=10)

        clear_button = tk.Button(action_frame, text="Clear Queue", font=button_font, bg="#DC3545", fg="white", command=self.clear_queue)
        clear_button.pack(side="right", padx=10)

    def add_inquiry(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        property_details = self.property_entry.get().strip()

        if not name or len(phone) != 10 or not phone.isdigit() or not property_details:
            messagebox.showerror("Input Error", "Invalid input. Please provide valid details.")
            return

        inquiry = {"name": name, "phone": phone, "property": property_details}
        self.inquiry_queue.append(inquiry)

        self.inquiry_table.insert("", "end", values=(name, phone, property_details))
        messagebox.showinfo("Inquiry Added", f"Inquiry added for {name} (Property: {property_details}).")
        self.clear_inputs()

    def process_inquiry(self):
        if not self.inquiry_queue:
            messagebox.showwarning("No Inquiries", "No inquiries to process.")
            return

        inquiry = self.inquiry_queue.popleft()

        # Find and delete the processed inquiry from the table
        for item in self.inquiry_table.get_children():
            if self.inquiry_table.item(item, "values")[1] == inquiry["phone"]:
                self.inquiry_table.delete(item)
                break

        messagebox.showinfo("Inquiry Processed", f"Processed Inquiry:\nName: {inquiry['name']}\nPhone: {inquiry['phone']}\nProperty: {inquiry['property']}")

    def clear_queue(self):
        if not self.inquiry_queue:
            messagebox.showwarning("No Inquiries", "Queue is already empty.")
            return

        self.inquiry_queue.clear()
        for item in self.inquiry_table.get_children():
            self.inquiry_table.delete(item)

        messagebox.showinfo("Queue Cleared", "All inquiries have been cleared.")

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.property_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
