import tkinter as tk
from tkinter import ttk, messagebox

# TreeNode Class to represent each node in the tree
class TreeNode:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.children = []  # A list to store children nodes

    def add_child(self, child_node):
        self.children.append(child_node)


# BinaryTree Class to manage the entire tree structure
class BinaryTree:
    def __init__(self):
        self.root = None

    def add_node(self, new_node):
        if self.root is None:
            self.root = new_node
        else:
            self._add(self.root, new_node)

    def _add(self, node, new_node):
        if new_node.name < node.name:
            if node.children and len(node.children) > 0:
                self._add(node.children[0], new_node)
            else:
                node.add_child(new_node)
        else:
            if len(node.children) == 2:
                self._add(node.children[1], new_node)
            else:
                node.add_child(new_node)

    def find_node(self, node, name):
        if node is None:
            return None
        if node.name == name:
            return node
        for child in node.children:
            found_node = self.find_node(child, name)
            if found_node:
                return found_node
        return None


# Application Class to create the GUI
class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Property Management")
        self.root.geometry("800x600")  # Initial size, but it will expand to fullscreen
        self.root.state("zoomed")  # Fullscreen
        self.root.resizable(True, True)  # Allow resizing
        self.tree = BinaryTree()

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=10, relief="flat", background="#4CAF50", foreground="white")
        style.configure("TLabel", font=("Arial", 12), padding=5)
        style.configure("TCombobox", font=("Arial", 12), padding=5)

        # Input Frame for adding property
        input_frame = ttk.LabelFrame(self.root, text="Add Property", width=800, height=200)
        input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Label(input_frame, text="Parent Property:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.parent_combo = ttk.Combobox(input_frame, values=["Industry", "Residential", "Commercial", "Retail"])
        self.parent_combo.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Property Name:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.category_combo = ttk.Combobox(input_frame, values=["Luxury", "Standard", "Economy"])
        self.category_combo.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        add_button = ttk.Button(input_frame, text="Add Property", command=self.add_property)
        add_button.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")

        # View Frame to show property tree
        view_frame = ttk.LabelFrame(self.root, text="View Property Tree", width=800, height=200)
        view_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.property_list = tk.Text(view_frame, height=10, width=80, font=("Arial", 12))
        self.property_list.grid(row=0, column=0, padx=20, pady=10)

        view_button = ttk.Button(view_frame, text="View Property Tree", command=self.view_tree)
        view_button.grid(row=1, column=0, pady=20, sticky="ew")

    def add_property(self):
        parent_name = self.parent_combo.get().strip()
        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()

        if not name or not category or not parent_name:
            messagebox.showerror("Input Error", "Please provide valid property details.")
            return

        # Check if the parent exists
        parent_node = self.tree.find_node(self.tree.root, parent_name)
        if parent_node:
            new_property = TreeNode(name, category)
            parent_node.add_child(new_property)
            messagebox.showinfo("Property Added", f"Property '{name}' added under {parent_name} ({category}).")
            self.clear_inputs()
        else:
            add_parent = messagebox.askyesno("Parent Not Found", f"Parent '{parent_name}' not found. Would you like to add it?")
            if add_parent:
                # Add the parent node
                new_parent = TreeNode(parent_name, "N/A")  # You can add a default category or leave it as "N/A"
                self.tree.add_node(new_parent)
                messagebox.showinfo("Parent Added", f"Parent '{parent_name}' has been added. Now you can add properties under it.")
            else:
                messagebox.showinfo("Operation Cancelled", "No changes were made.")

    def view_tree(self):
        if self.tree.root is None:
            messagebox.showinfo("Tree Empty", "No properties available.")
            return

        property_info = []
        self._view_tree(self.tree.root, property_info)
        self.property_list.delete(1.0, tk.END)
        self.property_list.insert(tk.END, "\n".join(property_info))

    def _view_tree(self, node, property_info, indent=""):
        if node is not None:
            property_info.append(f"{indent}{node.name} - {node.category}")
            for child in node.children:
                self._view_tree(child, property_info, indent + "  ")

    def clear_inputs(self):
        self.parent_combo.set("")
        self.name_entry.delete(0, tk.END)
        self.category_combo.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
