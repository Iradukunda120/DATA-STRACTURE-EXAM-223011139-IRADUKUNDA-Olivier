import tkinter as tk
from tkinter import ttk, messagebox


class BinaryTreeNode:
    """Node for the Binary Tree."""
    def __init__(self, order_id, name, phone, property_details, price):
        self.order_id = order_id
        self.name = name
        self.phone = phone
        self.property_details = property_details
        self.price = price
        self.left = None
        self.right = None


class BinaryTree:
    """Binary Tree to manage property orders."""
    def __init__(self):
        self.root = None

    def insert(self, order_id, name, phone, property_details, price):
        new_node = BinaryTreeNode(order_id, name, phone, property_details, price)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if new_node.price < current.price:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursive(current.right, new_node)

    def inorder_traversal(self, node=None, result=None):
        """Perform an in-order traversal to fetch all orders."""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node.left:
            self.inorder_traversal(node.left, result)
        result.append({
            "order_id": node.order_id,
            "name": node.name,
            "phone": node.phone,
            "property_details": node.property_details,
            "price": node.price
        })
        if node.right:
            self.inorder_traversal(node.right, result)
        return result


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Property Management (Binary Tree-Based)")
        self.root.state("zoomed")
        self.root.configure(bg="#F8F9FA")

        # Data Structure
        self.orders_tree = BinaryTree()
        self.order_id_counter = 1

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Fonts
        title_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Add Order", font=title_font, bg="#E9ECEF")
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

        tk.Label(input_frame, text="Price:", font=label_font, bg="#E9ECEF").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = ttk.Entry(input_frame)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5)

        add_button = tk.Button(input_frame, text="Add Order", font=button_font, bg="#28A745", fg="white", command=self.add_order)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Order Table Frame
        table_frame = tk.LabelFrame(self.root, text="Orders List(5 Orders)", font=title_font, bg="#E9ECEF")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.orders_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Phone", "Property", "Price"), show="headings", height=15)
        self.orders_table.heading("ID", text="Order ID")
        self.orders_table.heading("Name", text="Name")
        self.orders_table.heading("Phone", text="Phone Number")
        self.orders_table.heading("Property", text="Property Details")
        self.orders_table.heading("Price", text="Price")

        self.orders_table.column("ID", width=100, anchor="center")
        self.orders_table.column("Name", width=200, anchor="center")
        self.orders_table.column("Phone", width=150, anchor="center")
        self.orders_table.column("Property", width=300, anchor="center")
        self.orders_table.column("Price", width=100, anchor="center")
        self.orders_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Action Buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=20, pady=10)

        view_button = tk.Button(action_frame, text="View All Orders", font=button_font, bg="#007BFF", fg="white", command=self.view_orders)
        view_button.pack(side="left", padx=10)

    def add_order(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        property_details = self.property_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or len(phone) != 10 or not phone.isdigit() or not property_details or not price.isdigit():
            messagebox.showerror("Input Error", "Invalid input. Please provide valid details.")
            return

        order_id = self.order_id_counter
        price = int(price)

        self.orders_tree.insert(order_id, name, phone, property_details, price)
        self.order_id_counter += 1

        messagebox.showinfo("Order Added", f"Order {order_id} added for {name} (Property: {property_details}).")
        self.clear_inputs()

    def view_orders(self):
        orders = self.orders_tree.inorder_traversal()
        self.orders_table.delete(*self.orders_table.get_children())

        for order in orders:
            self.orders_table.insert("", "end", values=(order["order_id"], order["name"], order["phone"], order["property_details"], order["price"]))

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.property_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
