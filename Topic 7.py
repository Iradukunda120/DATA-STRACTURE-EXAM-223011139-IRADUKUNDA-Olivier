import tkinter as tk
from tkinter import ttk, messagebox

# TreeNode Class to represent each node in the tree
class TreeNode:
    def __init__(self, name, category, size, value, priority):
        self.name = name
        self.category = category
        self.size = size  # Property size (Small, Medium, Large)
        self.value = value  # Property value in monetary terms
        self.priority = priority  # Priority based on size or value
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

    def sort_properties_by_priority(self):
        # Perform Insertion Sort on the root's children based on priority
        if self.root:
            self.root.children = self.insertion_sort(self.root.children)
        for child in self.root.children:
            self.sort_child_nodes(child)

    def sort_child_nodes(self, node):
        if node.children:
            node.children = self.insertion_sort(node.children)
            for child in node.children:
                self.sort_child_nodes(child)

    def insertion_sort(self, nodes):
        # Insertion Sort algorithm to sort nodes based on priority
        for i in range(1, len(nodes)):
            key = nodes[i]
            j = i - 1
            while j >= 0 and key.priority < nodes[j].priority:
                nodes[j + 1] = nodes[j]
                j -= 1
            nodes[j + 1] = key
        return nodes


# Application Class to create the GUI
class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Property Management")
        self.root.geometry("800x600")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.tree = BinaryTree()

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=10, relief="flat", background="#4CAF50", foreground="black")
        style.configure("TLabel", font=("Arial", 12), padding=5)
        style.configure("TCombobox", font=("Arial", 12), padding=5)

        # Frame for input fields
        input_frame = ttk.LabelFrame(self.root, text="Add Property", width=800, height=250)
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

        ttk.Label(input_frame, text="Size:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.size_combo = ttk.Combobox(input_frame, values=["Small", "Medium", "Large"])
        self.size_combo.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Value (FRW):").grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.value_entry = ttk.Entry(input_frame)
        self.value_entry.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        add_button = ttk.Button(input_frame, text="Add Property", command=self.add_property)
        add_button.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

        # Frame to view the Property Tree
        view_frame = ttk.LabelFrame(self.root, text="View Property Tree", width=800, height=150)
        view_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.property_list = tk.Text(view_frame, height=5, width=80, font=("Arial", 12))
        self.property_list.grid(row=0, column=0, padx=20, pady=10)

        # View Property Tree button
        view_button = ttk.Button(view_frame, text="View Property Tree", command=self.view_tree)
        view_button.grid(row=1, column=0, pady=10, sticky="ew")

        # View Tree Button with a shortcut key (Alt + V)
        self.root.bind("<Alt-v>", self.view_tree)

    def add_property(self):
        parent_name = self.parent_combo.get().strip()
        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        size = self.size_combo.get().strip()
        value = self.value_entry.get().strip()

        if not name or not category or not parent_name or not size or not value:
            messagebox.showerror("Input Error", "Please provide valid property details.")
            return

        # Set priority based on Property Size (Size -> Large > Medium > Small)
        size_priority = {"Large": 1, "Medium": 2, "Small": 3}

        # Convert value to an integer and set priority based on size first
        size_priority_value = size_priority.get(size, 4)
        value = int(value)  # Convert value to integer
        priority = size_priority_value  # Here we use size priority, can include value as secondary factor

        # Check if the parent exists
        parent_node = self.tree.find_node(self.tree.root, parent_name)
        if parent_node:
            new_property = TreeNode(name, category, size, value, priority)
            parent_node.add_child(new_property)
            self.tree.sort_properties_by_priority()  # Sort after adding
            messagebox.showinfo("Property Added", f"Property '{name}' added under {parent_name} ({category}).")
            self.clear_inputs()
        else:
            add_parent = messagebox.askyesno("Parent Not Found", f"Parent '{parent_name}' not found. Would you like to add it?")
            if add_parent:
                # Add the parent node
                new_parent = TreeNode(parent_name, "N/A", "N/A", 0, 4)  # Default priority for parent node
                self.tree.add_node(new_parent)
                messagebox.showinfo("Parent Added", f"Parent '{parent_name}' has been added. Now you can add properties under it.")
            else:
                messagebox.showinfo("Operation Cancelled", "No changes were made.")

    def view_tree(self, event=None):
        if self.tree.root is None:
            messagebox.showinfo("Tree Empty", "No properties available.")
            return

        property_info = []
        self._view_tree(self.tree.root, property_info)
        self.property_list.delete(1.0, tk.END)
        self.property_list.insert(tk.END, "\n".join(property_info))

    def _view_tree(self, node, property_info, indent=""):
        if node is not None:
            property_info.append(f"{indent}{node.name} - {node.category} (Size: {node.size}, Value: {node.value} FRW, Priority: {node.priority})")
            for child in node.children:
                self._view_tree(child, property_info, indent + "  ")

    def clear_inputs(self):
        self.parent_combo.set("")
        self.name_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.size_combo.set("")
        self.value_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
