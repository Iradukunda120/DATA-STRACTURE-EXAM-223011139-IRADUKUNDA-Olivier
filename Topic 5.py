import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Node:
    def __init__(self, order_id, name, phone, property_details, price):
        self.order_id = order_id
        self.name = name
        self.phone = phone
        self.property_details = property_details
        self.price = price
        self.next = None

class CircularLinkedList:
    def __init__(self, limit=5):
        self.head = None
        self.tail = None
        self.size = 0
        self.limit = limit

    def insert(self, order_id, name, phone, property_details, price):
        new_node = Node(order_id, name, phone, property_details, price)
        if self.size >= self.limit:
            self.remove_front()
        
        if not self.head:
            self.head = self.tail = new_node
            self.head.next = self.head
        else:
            self.tail.next = new_node
            new_node.next = self.head
            self.tail = new_node
        
        self.size += 1

    def remove_front(self):
        if not self.head:
            return
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head
        self.size -= 1

    def remove_by_id(self, order_id):
        if not self.head:
            return False

        current = self.head
        prev = self.tail

        while True:
            if current.order_id == order_id:
                if current == self.head:
                    self.remove_front()
                else:
                    prev.next = current.next
                    if current == self.tail:
                        self.tail = prev
                    self.size -= 1
                return True
            prev = current
            current = current.next
            if current == self.head:
                break
        return False

    def to_list(self):
        data = []
        if not self.head:
            return data

        current = self.head
        while True:
            data.append({
                "order_id": current.order_id,
                "name": current.name,
                "phone": current.phone,
                "property_details": current.property_details,
                "price": current.price
            })
            current = current.next
            if current == self.head:
                break
        return data

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Property Management System")
        self.root.state('zoomed')  # Maximize the window
        self.root.configure(bg="#f0f8ff")  # Light blue background

        self.orders_list = CircularLinkedList(limit=5)
        self.order_id_counter = 1

        self.create_ui()

    def create_ui(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Order", style="TFrame")
        input_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(input_frame, text="Name:", font=("Arial", 12, "bold"), foreground="black").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Phone:", font=("Arial", 12, "bold"), foreground="black").grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Property Details:", font=("Arial", 12, "bold"), foreground="black").grid(row=2, column=0, padx=10, pady=10)
        self.property_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.property_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Price:", font=("Arial", 12, "bold"), foreground="black").grid(row=3, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        add_button = ttk.Button(input_frame, text="Add Order", command=self.add_order, style="AddOrder.TButton")
        add_button.grid(row=4, column=0, columnspan=2, pady=15)

        # Orders List
        orders_frame = ttk.LabelFrame(self.root, text="Order List", style="TFrame")
        orders_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.orders_table = ttk.Treeview(
            orders_frame, 
            columns=("ID", "Name", "Phone", "Property", "Price"), 
            show="headings",
            style="Custom.Treeview",
            height=5  # Minimize height to show just 5 rows
        )
        self.orders_table.heading("ID", text="Order ID")
        self.orders_table.heading("Name", text="Name")
        self.orders_table.heading("Phone", text="Phone")
        self.orders_table.heading("Property", text="Property Details")
        self.orders_table.heading("Price", text="Price")
        self.orders_table.pack(fill="both", expand=True)

        # Action Buttons Frame
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=20, pady=10)

        view_button = ttk.Button(action_frame, text="View Orders", command=self.update_order_list, style="ViewOrder.TButton")
        view_button.pack(side="left", padx=10)

        remove_button = ttk.Button(action_frame, text="Remove Order by ID", command=self.prompt_remove_order, style="RemoveOrder.TButton")
        remove_button.pack(side="left", padx=10)

        clear_button = ttk.Button(action_frame, text="Clear All Orders", command=self.clear_orders, style="ClearOrder.TButton")
        clear_button.pack(side="right", padx=10)

    def add_order(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        property_details = self.property_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or len(phone) != 10 or not phone.isdigit() or not property_details or not price.isdigit():
            messagebox.showerror("Input Error", "Invalid input. Please provide valid details.")
            return

        price = int(price)
        order_id = self.order_id_counter

        self.orders_list.insert(order_id, name, phone, property_details, price)
        self.order_id_counter += 1
        messagebox.showinfo("Order Added", f"Order {order_id} added for {name} (Property: {property_details}).")
        self.clear_inputs()
        self.update_order_list()

    def update_order_list(self):
        for item in self.orders_table.get_children():
            self.orders_table.delete(item)

        orders = self.orders_list.to_list()
        for order in orders:
            self.orders_table.insert("", tk.END, values=(order["order_id"], order["name"], order["phone"], order["property_details"], order["price"]))

    def prompt_remove_order(self):
        order_id = simpledialog.askinteger("Remove Order", "Enter Order ID to remove:")
        if order_id is None:
            return
        removed = self.orders_list.remove_by_id(order_id)
        if removed:
            messagebox.showinfo("Order Removed", f"Order {order_id} has been removed.")
        else:
            messagebox.showerror("Order Not Found", f"No order found with ID {order_id}.")
        self.update_order_list()

    def clear_orders(self):
        self.orders_list.clear()
        self.update_order_list()
        messagebox.showinfo("Orders Cleared", "All orders have been cleared.")

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.property_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TFrame", background="#f0f8ff", font=("Arial", 14), foreground="black")
    style.configure("AddOrder.TButton", background="green", foreground="black", font=("Arial", 12, "bold"))
    style.configure("ViewOrder.TButton", background="blue", foreground="black", font=("Arial", 12, "bold"))
    style.configure("RemoveOrder.TButton", background="red", foreground="black", font=("Arial", 12, "bold"))
    style.configure("ClearOrder.TButton", background="orange", foreground="black", font=("Arial", 12, "bold"))
    style.configure("Custom.Treeview", rowheight=30, font=("Arial", 12, "bold"), foreground="black")
    app = RealEstateApp(root)
    root.mainloop()
