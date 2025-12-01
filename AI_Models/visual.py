
import tkinter as tk
from tkinter import messagebox
#import matplotlib.pyplot as plt
from typing import List, Dict

class DataVisualizer:
    def __init__(self):
        self.data = []
        


    def submit(self):
        # Create window
        root = tk.Tk()
        root.title("Product Input")

        # Create label
        label = tk.Label(root, text="Enter Product Name:")
        label.pack(pady=10)

        # Create input field
        entry = tk.Entry(root, width=40)
        entry.pack(pady=5)

        # Submit button
        #submit_button = tk.Button(root, text="Submit", command='submit')
        #submit_button.pack(pady=10)

        # Run the window loop
        root.mainloop()    

        product_name = entry.get()
        messagebox.showinfo("Product Entered", f"You entered: {product_name}")
        print("Product Name:", product_name)




    def get_user_input(self):
        root = tk.Tk()
        root.title("Enter Product Name: ")
        user_input = tk.simpledialog.askstring("Enter Product Name: ")
        root.destroy()
        return user_input

    def show_analysis_result(self, result: list[Dict]):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Analysis Result", result)
        root.destroy()


if __name__ == "__main__":
    visualizer = DataVisualizer()
    visualizer.submit()