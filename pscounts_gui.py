# pscounts_gui.py
"""
Control Panel Module

This module implements the graphical user interface (GUI) for the PSCounts application.
It uses Tkinter's ttk module for a modern look and is organized as a class (ShiftLoggerApp)
to demonstrate object-oriented programming. It includes input validation, event handling,
and a sample of basic graphics using a Canvas.

The code demonstrates many Python basics:
 - Variables and expressions
 - Data types (strings, integers, lists, dictionaries)
 - Branching (if/else)
 - Loops
 - Functions and methods
 - Exception handling
 - File I/O (through imported modules)
 - Classes and inheritance (via our data module)
 - Recursion (in the data module example)
 - Plotting (with matplotlib)
 - Searching and string formatting
 - Basic graphics with Tkinter Canvas
 - Conversions between types
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
import pscounts_data as data    # Import the data module for file operations.
import pscounts_stats as stats  # Import the stats module for data analysis and plotting.
import logging                # For logging debug messages.
import pdb                    # Optional: For debugging (e.g., use pdb.set_trace() to step through code)

# Set up logging for debugging.
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_numeric(new_value):
    """
    Validation function for numeric input.
    Allows empty string (to clear a field) or only digits.
    This ensures that only valid numbers are entered.
    """
    if new_value == "":
        return True
    return new_value.isdigit()

class ShiftLoggerApp:
    """
    The main GUI application class.
    This class creates and manages the window for entering shift data.
    It demonstrates object-oriented programming by grouping related widgets
    and functionality into methods.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Shift Logger for Problem Solve Department")
        
        # Configure ttk style for a modern look.
        self.style = ttk.Style()
        self.style.theme_use("clam")  # "clam" is one of several built-in themes.
        
        # Instance variables to hold user input values.
        self.shift_type_var = tk.StringVar(value="Day")
        self.shift_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.selected_quarter_var = tk.StringVar(value=data.QUARTERS[0])
        self.rsp_total_var = tk.StringVar(value="0")
        self.rsp_headcount_total_var = tk.StringVar(value="0")
        self.non_rsp_headcount_total_var = tk.StringVar(value="0")
        
        # Dictionaries to store input fields for each section.
        self.rsp_entries = {}
        self.dock_entries = {}
        self.dmg_entries = {}
        self.other_entries = {}
        
        # This attribute will hold delta analysis data.
        self.delta_df_global = None
        
        # Build the complete GUI.
        self.build_gui()
    
    def build_gui(self):
        """Construct the full GUI layout using ttk widgets."""
        # Create a main frame with a canvas and scrollbar for scrolling.
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self.scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Top Frame: Shift info and buttons.
        top_frame = ttk.Frame(self.scrollable_frame, padding=10)
        top_frame.pack(fill="x")
        ttk.Label(top_frame, text="Shift Type (Day/Night):").grid(row=0, column=0, sticky="w")
        ttk.Entry(top_frame, textvariable=self.shift_type_var, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(top_frame, text="Shift Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w")
        ttk.Entry(top_frame, textvariable=self.shift_date_var, width=12).grid(row=0, column=3, padx=5)
        # Button to import files; calls self.on_import_files
        ttk.Button(top_frame, text="Import Files", command=self.on_import_files).grid(row=0, column=4, padx=10)
        ttk.Button(top_frame, text="Open Delta Summary", command=self.open_delta_summary_window).grid(row=0, column=5, padx=10)
        
        # Middle Frame: Quarter selection.
        mid_frame = ttk.Frame(self.scrollable_frame, padding=10)
        mid_frame.pack(fill="x")
        ttk.Label(mid_frame, text="Select Quarter:").grid(row=0, column=0, sticky="w")
        self.quarter_menu = ttk.OptionMenu(mid_frame, self.selected_quarter_var, data.QUARTERS[0], *data.QUARTERS)
        self.quarter_menu.grid(row=0, column=1, padx=5)
        
        # Data Entry Frame.
        data_frame = ttk.Frame(self.scrollable_frame, padding=10)
        data_frame.pack(fill="both", expand=True)
        
        # RSP Floors Section.
        ttk.Label(data_frame, text="RSP Floors (Enter counts below)", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=7, pady=5)
        for idx, floor in enumerate(data.RSP_FLOORS):
            self.rsp_entries[floor] = {}
            ttk.Label(data_frame, text=f"RSP {floor}:").grid(row=idx+2, column=0, sticky="e", padx=3)
            for jdx, metric in enumerate(data.RSP_METRICS):
                # Create an entry with validation for numeric input.
                vcmd = (self.master.register(validate_numeric), '%P')
                var = tk.StringVar()
                self.rsp_entries[floor][metric] = var
                entry = ttk.Entry(data_frame, textvariable=var, width=8, validate="key", validatecommand=vcmd)
                entry.grid(row=idx+2, column=jdx+1, padx=3, pady=2)
                if metric == "Headcount":
                    var.trace_add("write", self.update_headcount_totals)
                elif metric == "Piles":
                    var.trace_add("write", self.update_rsp_total)
        row_idx = len(data.RSP_FLOORS) + 2
        ttk.Label(data_frame, text="RSP Total (Piles):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
        ttk.Entry(data_frame, textvariable=self.rsp_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
        row_idx += 1
        ttk.Label(data_frame, text="RSP Total (Headcount):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
        ttk.Entry(data_frame, textvariable=self.rsp_headcount_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
        row_idx += 1
        ttk.Label(data_frame, text="Non-RSP Total (Headcount):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
        ttk.Entry(data_frame, textvariable=self.non_rsp_headcount_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
        row_idx += 2
        
        # Dock Section.
        ttk.Label(data_frame, text="Dock (Enter counts)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=8, pady=5)
        row_idx += 1
        self.dock_entries = {}
        for jdx, metric in enumerate(data.DOCK_METRICS):
            ttk.Label(data_frame, text=metric, font=("Arial", 10, "underline")).grid(row=row_idx, column=jdx+1, padx=3, pady=3)
        row_idx += 1
        ttk.Label(data_frame, text="Dock:").grid(row=row_idx, column=0, sticky="e", padx=3)
        for jdx, metric in enumerate(data.DOCK_METRICS):
            vcmd = (self.master.register(validate_numeric), '%P')
            var = tk.StringVar()
            self.dock_entries[metric] = var
            entry = ttk.Entry(data_frame, textvariable=var, width=8, validate="key", validatecommand=vcmd)
            entry.grid(row=row_idx, column=jdx+1, padx=3, pady=2)
            if metric == "Headcount":
                var.trace_add("write", self.update_headcount_totals)
        row_idx += 2
        
        # Damageland Section.
        ttk.Label(data_frame, text="Damageland (Enter counts)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=6, pady=5)
        row_idx += 1
        self.dmg_entries = {}
        for jdx, metric in enumerate(data.DAMAGELAND_METRICS):
            ttk.Label(data_frame, text=metric, font=("Arial", 10, "underline")).grid(row=row_idx, column=jdx+1, padx=3, pady=3)
        row_idx += 1
        ttk.Label(data_frame, text="Damageland:").grid(row=row_idx, column=0, sticky="e", padx=3)
        for jdx, metric in enumerate(data.DAMAGELAND_METRICS):
            vcmd = (self.master.register(validate_numeric), '%P')
            var = tk.StringVar()
            self.dmg_entries[metric] = var
            entry = ttk.Entry(data_frame, textvariable=var, width=8, validate="key", validatecommand=vcmd)
            entry.grid(row=row_idx, column=jdx+1, padx=3, pady=2)
            if metric == "Headcount":
                var.trace_add("write", self.update_headcount_totals)
        row_idx += 2
        
        # Other Roles Section.
        ttk.Label(data_frame, text="Other Roles (Headcount Only)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=3, pady=5)
        row_idx += 1
        self.other_entries = {}
        for role in data.OTHER_ROLES:
            ttk.Label(data_frame, text=f"{role}:").grid(row=row_idx, column=0, sticky="e", padx=3)
            vcmd = (self.master.register(validate_numeric), '%P')
            var = tk.StringVar()
            self.other_entries[role] = var
            entry = ttk.Entry(data_frame, textvariable=var, width=8, validate="key", validatecommand=vcmd)
            entry.grid(row=row_idx, column=1, padx=3, pady=2)
            var.trace_add("write", self.update_headcount_totals)
            row_idx += 1
        
        # Submit Button.
        ttk.Button(self.scrollable_frame, text="Submit", command=self.submit_data).pack(pady=10)
        # Button to show basic graphics (demonstrates Canvas drawing).
        ttk.Button(self.scrollable_frame, text="Show Sample Graphics", command=self.draw_sample_graphics).pack(pady=5)
    
    def on_import_files(self):
        """
        Open a file dialog to select Excel files and import the data.
        This method is called when the user clicks the "Import Files" button.
        """
        try:
            file_paths = filedialog.askopenfilenames(
                title="Select up to 5 Excel files to import",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if file_paths:
                latest_file = data.import_data_from_excel_files(file_paths)
                messagebox.showinfo("Import Successful", f"Data imported from:\n{latest_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data:\n{e}")
    
    def update_headcount_totals(self, *args):
        """Update the headcount totals for RSP and non-RSP areas."""
        total_rsp = 0
        for floor in data.RSP_FLOORS:
            try:
                val = self.rsp_entries[floor]["Headcount"].get().strip()
                if val.isdigit():
                    total_rsp += int(val)
            except KeyError:
                continue
        self.rsp_headcount_total_var.set(str(total_rsp))
        
        total_non_rsp = 0
        try:
            val = self.dock_entries["Headcount"].get().strip()
            if val.isdigit():
                total_non_rsp += int(val)
        except KeyError:
            pass
        try:
            val = self.dmg_entries["Headcount"].get().strip()
            if val.isdigit():
                total_non_rsp += int(val)
        except KeyError:
            pass
        for role in data.OTHER_ROLES:
            try:
                val = self.other_entries[role].get().strip()
                if val.isdigit():
                    total_non_rsp += int(val)
            except KeyError:
                continue
        self.non_rsp_headcount_total_var.set(str(total_non_rsp))
    
    def update_rsp_total(self, *args):
        """Update the total 'Piles' for RSP floors."""
        total = 0
        for floor in data.RSP_FLOORS:
            try:
                val = self.rsp_entries[floor]["Piles"].get().strip()
                if val.isdigit():
                    total += int(val)
            except KeyError:
                continue
        self.rsp_total_var.set(str(total))
    
    def collect_data(self):
        """
        Collect all entered data and compile it into a list of records.
        Each record is a dictionary representing one row of data.
        """
        records = []
        current_quarter = self.selected_quarter_var.get()
        for floor in data.RSP_FLOORS:
            rec = {"Quarter": current_quarter, "Role": f"RSP ({floor})", "Floor": floor}
            for metric in data.RSP_METRICS:
                val = self.rsp_entries[floor][metric].get().strip()
                rec[metric] = int(val) if (val and val.isdigit()) else None
            records.append(rec)
        total_piles = sum(int(self.rsp_entries[floor]["Piles"].get().strip()) for floor in data.RSP_FLOORS 
                          if self.rsp_entries[floor]["Piles"].get().strip().isdigit())
        records.append({"Quarter": current_quarter, "Role": "RSP (Total)", "Floor": "", "Piles": total_piles})
        try:
            total_rsp_headcount = int(self.rsp_headcount_total_var.get())
        except:
            total_rsp_headcount = 0
        records.append({"Quarter": current_quarter, "Role": "RSP (Headcount Total)", "Floor": "", "Headcount": total_rsp_headcount})
        rec = {"Quarter": current_quarter, "Role": "Dock", "Floor": ""}
        for metric in data.DOCK_METRICS:
            val = self.dock_entries[metric].get().strip()
            rec[metric] = int(val) if (val and val.isdigit()) else None
        records.append(rec)
        rec = {"Quarter": current_quarter, "Role": "Damageland", "Floor": ""}
        for metric in data.DAMAGELAND_METRICS:
            val = self.dmg_entries[metric].get().strip()
            rec[metric] = int(val) if (val and val.isdigit()) else None
        records.append(rec)
        for role in data.OTHER_ROLES:
            rec = {"Quarter": current_quarter, "Role": role, "Floor": ""}
            val = self.other_entries[role].get().strip()
            rec["Headcount"] = int(val) if (val and val.isdigit()) else None
            records.append(rec)
        try:
            total_non_rsp_headcount = int(self.non_rsp_headcount_total_var.get())
        except:
            total_non_rsp_headcount = 0
        records.append({"Quarter": current_quarter, "Role": "Non-RSP (Headcount Total)", "Floor": "", "Headcount": total_non_rsp_headcount})
        return records
    
    def clear_fields(self):
        """Clear all input fields so the form is ready for new data."""
        for floor in data.RSP_FLOORS:
            for metric in data.RSP_METRICS:
                self.rsp_entries[floor][metric].set("")
        for metric in data.DOCK_METRICS:
            self.dock_entries[metric].set("")
        for metric in data.DAMAGELAND_METRICS:
            self.dmg_entries[metric].set("")
        for role in data.OTHER_ROLES:
            self.other_entries[role].set("")
        self.rsp_total_var.set("0")
        self.rsp_headcount_total_var.set("0")
        self.non_rsp_headcount_total_var.set("0")
    
    def submit_data(self):
        """
        Process form submission:
         - Collect data
         - Determine the Excel file path and create workbook if needed
         - Save data to Excel and update summary sheets
         - Adjust Excel columns
         - Show a success message and clear the form
        """
        records = self.collect_data()
        if records is None:
            return
        file_path = data.get_excel_file_path(self.shift_date_var.get(), self.shift_type_var.get())
        if not os.path.exists(file_path):
            data.create_new_workbook(file_path)
        try:
            data.save_quarter_to_excel(self.selected_quarter_var.get(), records, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data to Excel:\n{e}")
            return
        try:
            data.aggregate_data(file_path, current_quarter=self.selected_quarter_var.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update EoS sheet:\n{e}")
            return
        try:
            data.update_shift_changes_summary(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update Shift Changes summary:\n{e}")
            return
        try:
            data.adjust_excel_columns(file_path)
        except Exception as e:
            messagebox.showwarning("Warning", f"Data saved, but adjusting columns failed:\n{e}")
        messagebox.showinfo("Success", f"Data for {self.selected_quarter_var.get()} saved successfully!")
        try:
            data.load_data_from_json()
        except Exception as e:
            messagebox.showwarning("Warning", f"Data reloading warning:\n{e}")
        self.clear_fields()
    
    def show_graphs(self):
        """
        Display a line graph showing the trend of RSP Total Piles over the quarters.
        """
        available_quarters = [q for q in data.QUARTERS if q in data.shift_data and "RSP (Total)" in data.shift_data[q]]
        if not available_quarters:
            return
        x = list(range(len(available_quarters)))
        y = []
        for q in available_quarters:
            try:
                val = int(data.shift_data[q]["RSP (Total)"].get("Piles", 0))
            except Exception:
                val = 0
            y.append(val)
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6,4))
        plt.plot(x, y, marker="o", linestyle="-", color="blue")
        plt.xticks(x, available_quarters)
        plt.xlabel("Quarter")
        plt.ylabel("RSP Total Piles")
        plt.title("Trend of RSP Total Piles Over Quarters")
        plt.tight_layout()
        plt.show()
    
    def open_delta_summary_window(self):
        """
        Open a new window for delta analysis.
        This window lets you select two quarters, choose a graph type,
        generate a text summary of differences, and view a graph for a selected metric.
        """
        delta_win = tk.Toplevel(self.master)
        delta_win.title("Delta Summary Analysis")
        
        instructions = (
            "Instructions:\n"
            "1. Select two quarters to compare.\n"
            "2. Choose the graph type (Bar or Line).\n"
            "3. Click 'Generate Delta' to compute differences.\n"
            "4. Use the 'Select Metric' dropdown to choose a metric.\n"
            "5. Click 'Show Graph' to view a graph of the differences.\n"
            "6. Percent changes are shown along with absolute differences."
        )
        ttk.Label(delta_win, text=instructions, foreground="blue", justify="left").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        ttk.Label(delta_win, text="Select Quarter 1:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        q1_var = tk.StringVar(value=data.QUARTERS[0])
        ttk.OptionMenu(delta_win, q1_var, data.QUARTERS[0], *data.QUARTERS).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(delta_win, text="Select Quarter 2:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        q2_var = tk.StringVar(value=data.QUARTERS[1] if len(data.QUARTERS) > 1 else data.QUARTERS[0])
        ttk.OptionMenu(delta_win, q2_var, data.QUARTERS[1] if len(data.QUARTERS) > 1 else data.QUARTERS[0], *data.QUARTERS).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(delta_win, text="Graph Type:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        graph_type_var = tk.StringVar(value="Bar")
        ttk.OptionMenu(delta_win, graph_type_var, "Bar", "Bar", "Line").grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(delta_win, text="Select Metric:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        metric_var = tk.StringVar(value="")
        metric_menu = ttk.OptionMenu(delta_win, metric_var, "")
        metric_menu.grid(row=4, column=1, padx=5, pady=5)
        
        delta_text = tk.Text(delta_win, height=10, width=80)
        delta_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        delta_text.config(state="disabled")
        
        self.delta_df_global = None  # Reset delta data
        
        def generate_delta():
            """Compute differences between the selected quarters and update the text summary."""
            summary, df = stats.compute_deltas_between(q1_var.get(), q2_var.get())
            self.delta_df_global = df
            delta_text.config(state="normal")
            delta_text.delete("1.0", tk.END)
            delta_text.insert(tk.END, summary)
            delta_text.config(state="disabled")
            menu = metric_menu["menu"]
            menu.delete(0, "end")
            if not df.empty:
                metrics = df["Metric"].unique().tolist()
                if metrics:
                    metric_var.set(metrics[0])
                    for m in metrics:
                        menu.add_command(label=m, command=lambda value=m: metric_var.set(value))
        
        def show_delta_graph():
            """Plot a graph for the selected metric."""
            if self.delta_df_global is None or self.delta_df_global.empty:
                messagebox.showerror("Error", "Please generate delta data first.")
                return
            try:
                stats.plot_difference(self.delta_df_global, metric_var.get(), q1_var.get(), q2_var.get(), graph_type_var.get())
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def show_help():
            """Display help instructions for the Delta Summary window."""
            help_message = (
                "Delta Summary Help:\n"
                "- Select two quarters from the dropdown menus.\n"
                "- Choose a graph type (Bar or Line).\n"
                "- Click 'Generate Delta' to calculate differences.\n"
                "- The text box shows differences and percent changes.\n"
                "- Use the 'Select Metric' dropdown to pick a metric, then click 'Show Graph' to see the graph."
            )
            messagebox.showinfo("Delta Summary Help", help_message)
        
        ttk.Button(delta_win, text="Generate Delta", command=generate_delta).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(delta_win, text="Show Graph", command=show_delta_graph).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(delta_win, text="Help", command=show_help).grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    
    def draw_sample_graphics(self):
        """
        Demonstrate basic graphics by drawing a simple rectangle on a Canvas.
        """
        graphic_win = tk.Toplevel(self.master)
        graphic_win.title("Basic Graphics Example")
        canvas = tk.Canvas(graphic_win, width=300, height=200, bg="white")
        canvas.pack()
        # Draw a rectangle: top-left (50,50) to bottom-right (250,150)
        canvas.create_rectangle(50, 50, 250, 150, outline="black", fill="lightblue")
        canvas.create_text(150, 100, text="Hello, Graphics!", fill="black", font=("Arial", 14))
        logging.debug("Basic graphics drawn.")
    
    def run(self):
        """Start the main event loop."""
        self.master.mainloop()

# End of ShiftLoggerApp class.