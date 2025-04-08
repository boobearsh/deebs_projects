#!/usr/bin/env python3  # This "shebang" line is used on Unix/Linux systems to indicate which interpreter should run the script (Python 3 in this case).
"""
PSCounts.py - Beta 1.2

Shift Logger for Problem Solve Department

Overview:
---------
This program allows users (even those with little or no coding experience) to record
and update shift counts for various roles. Data is saved into an Excel workbook 
with these sheets:
    • SoS – Start of Shift counts
    • Q1, Q2, Q3 – Data for intermediate quarters
    • EoS – End of Shift counts (formatted like the other sheets, with the most up-to-date counts for EoS)
    • Wash – (Empty; reserved for future use)
    • Shift Changes – A summary of changes for management review

Key Improvements in this Revision:
-----------------------------------
1. **EoS Sheet Formatting and Data:**  
   - The EoS sheet now looks like the other sheets (same columns, no "Quarter" column).  
   - When data is submitted for the EoS quarter, the sheet shows those counts directly rather than an aggregated total.

2. **Shift Changes Sheet Formatting:**  
   - The Shift Changes sheet is sorted by quarter (using a custom order) and by role so that management has a clear, easy-to-read overview of all changes.

To run, simply execute:
    python PSCounts.py
"""
# -------------------------------
# Global Variables and Configuration
# -------------------------------

# List of shift quarters (from start-of-shift to end-of-shift)
QUARTERS = ["SoS", "Q1", "Q2", "Q3", "EoS"]  # These are the names of the time periods (quarters) tracked.

# RSP floors and the metrics for each floor
RSP_FLOORS = ["A2", "A3", "A4", "B2", "B3", "B4"]  # These are the floor codes in the RSP area (Problem Solve area).
RSP_METRICS = ["Headcount", "Piles", "Damages", "LAF", "ISS", "NONCON"]  # Metrics to record for each RSP floor.

# Metrics for Dock, Damageland, and other roles
DOCK_METRICS = ["Headcount", "Piles", "Liquid Damages", "Dry Damages", "LAF", "ISS", "NC"]  # Metrics for the Dock area.
DAMAGELAND_METRICS = ["Headcount", "Backlog", "Damage Stow", "Received", "Deletes"]  # Metrics for the Damageland area.
OTHER_ROLES = ["Customer Returns", "Inbound Support Services (ICQA)", "IOL", "GK"]  # Other roles (these only require Headcount metric).

# JSON file used to store/merge shift data between runs
DATA_JSON = "shift_data.json"  # Filename for the JSON file that saves shift data.

# Global dictionary to hold shift data loaded from or saved to JSON
shift_data = {}  # Initialize an empty dictionary to keep shift data in memory.

# -------------------------------
# File and Data Management Functions
# -------------------------------

def save_data_to_json(data):
    """Save the current shift data dictionary to a JSON file on disk.
    This allows the program to preserve data between runs (so data isn't lost when the program closes).
    It is typically called after data is updated or imported, to save the latest state.
    """
    try:
        with open(DATA_JSON, "w") as f:  # Open (or create) the JSON file in write mode as file object f
            json.dump(data, f, indent=4)  # Write the 'data' dictionary to the file in JSON format, with indentation for readability
    except Exception as e:
        messagebox.showerror("Error", f"Could not save JSON data:\n{e}")  # If any error occurs during file writing, show an error message

def load_data_from_json():
    """Load previously saved shift data from the JSON file into the global shift_data dictionary.
    This allows the program to start with data from last session if available.
    """
    global shift_data  # Use the global variable defined above
    if os.path.exists(DATA_JSON):  # Only attempt to load if the JSON file actually exists
        try:
            with open(DATA_JSON, "r") as f:  # Open the JSON file in read mode as f
                shift_data = json.load(f)  # Load the JSON content into the shift_data dictionary
        except Exception as e:
            messagebox.showerror("Error", f"Could not load JSON data:\n{e}")  # If there's an error (e.g., file is corrupted), show an error message

def get_excel_file_path(shift_date, shift_type):
    """
    Generate a file path for the Excel workbook based on the provided shift date and type.
    It will create an 'exports/<date>' folder if it doesn't exist and return the path 
    to the Excel file named with the shift type (Day/Night) and date.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Find the directory where this script file is located
    exports_dir = os.path.join(script_dir, "exports")  # Path to an "exports" folder within the script directory
    os.makedirs(exports_dir, exist_ok=True)  # Create the exports folder if it doesn't exist (no error if it already exists)
    folder = os.path.join(exports_dir, shift_date)  # Path to a subfolder named after the shift_date inside exports
    os.makedirs(folder, exist_ok=True)  # Create the date-named folder if it doesn't exist
    filename = f"InboundPS_{'Days' if shift_type.lower()=='day' else 'Nights'}{shift_date}.xlsx"  # File name: includes "Days" or "Nights" depending on shift_type, plus the date
    return os.path.join(folder, filename)  # Full path to the Excel file that will store the data

def create_new_workbook(file_path):
    """Create a brand new Excel workbook file with all the required sheets for this application.
    Used when starting a new log for a date that doesn't have an Excel file yet.
    """
    wb = Workbook()  # Create a new Excel workbook in memory (using openpyxl)
    ws = wb.active  # Get the default first worksheet of this new workbook
    ws.title = "SoS"  # Rename the first sheet to "SoS" (Start of Shift)
    # Create additional sheets for each quarter and other needed categories
    for sheet in ["Q1", "Q2", "Q3", "EoS", "Wash", "Shift Changes"]:
        wb.create_sheet(title=sheet)  # Add a new sheet with this title
    wb.save(file_path)  # Save the new workbook to the specified file path (creates the .xlsx file on disk)

def import_files():
    """
    Allow the user to select up to 5 Excel files to import data from.
    Data from the most recent selected file is loaded into the global shift_data dictionary.
    """
    files = filedialog.askopenfilenames(title="Select up to 5 Excel files to import",
                                        filetypes=[("Excel files", "*.xlsx")])
    if not files:  # If the user canceled or selected nothing
        return  # Exit the function; nothing to import
    files = list(files)  # Convert the tuple of file paths to a list (easier to handle)
    # Ensure all selected files are from the same folder (to avoid mixing data from different dates)
    if len(set(os.path.dirname(f) for f in files)) != 1:
        messagebox.showerror("Error", "Please select files from the same folder.")
        return
    latest_file = max(files, key=os.path.getmtime)  # Pick the file with the latest modification time (the newest file)
    try:
        wb = load_workbook(latest_file)  # Load the latest Excel file as a workbook
        for q in QUARTERS:  # Loop through each quarter name (sheet name) we care about
            if q in wb.sheetnames:  # If the sheet for that quarter exists in the workbook
                df = pd.read_excel(latest_file, sheet_name=q)  # Read that sheet into a pandas DataFrame
                if not df.empty and "Role" in df.columns:  # If the sheet is not empty and contains a "Role" column (valid data)
                    quarter_dict = {}  # Prepare a dictionary to hold data for this quarter
                    for _, row in df.iterrows():  # Iterate over each row in the DataFrame
                        role = row["Role"]  # The role name in this row (e.g., "RSP (A2)" or "Dock")
                        quarter_dict[role] = row.to_dict()  # Convert the entire row to a dict and store it under that role name
                    shift_data[q] = quarter_dict  # Save the quarter's data dictionary in the global shift_data under key q
        save_data_to_json(shift_data)  # Save the combined data to JSON file for persistence
        messagebox.showinfo("Import Successful", f"Data imported from:\n{latest_file}")  # Inform the user that import was successful
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import file:\n{e}")  # If anything goes wrong during import, show an error

# -------------------------------
# Excel Sheet Update Functions
# -------------------------------

def save_quarter_to_excel(quarter, records, file_path):
    """
    Write (or overwrite) the records for a specific quarter to the Excel workbook.
    For the EoS sheet, the "Quarter" column is removed to match the format of other sheets.
    """
    df = pd.DataFrame(records)  # Create a DataFrame from the list of record dictionaries
    if quarter == "EoS" and "Quarter" in df.columns:
        df = df.drop(columns=["Quarter"])  # Remove the Quarter column for EoS data (so EoS sheet has no quarter column)
    # Open an Excel writer in append mode; if the sheet exists, replace its contents
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=quarter, index=False)  # Write the DataFrame to the sheet named after the quarter (no index column)

def aggregate_data(file_path, current_quarter):
    """
    Update the EoS sheet after a submission:
      - If the current quarter is "EoS", just ensure the EoS sheet reflects the submitted data (no aggregation, and remove "Quarter" column).
      - Otherwise (if current quarter is SoS, Q1, Q2, or Q3), aggregate data from SoS through Q3 to produce an updated EoS summary.
    """
    if current_quarter == "EoS":
        df = pd.read_excel(file_path, sheet_name="EoS")  # Read the EoS sheet data into a DataFrame
        if "Quarter" in df.columns:
            df = df.drop(columns=["Quarter"])  # Drop the Quarter column to make EoS sheet consistent with others
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name="EoS", index=False)  # Write back the cleaned EoS DataFrame to the Excel file
    else:
        try:
            wb = load_workbook(file_path)  # Load the workbook to gather data from multiple sheets
            dataframes = []
            for sheet_name in ["SoS", "Q1", "Q2", "Q3"]:
                if sheet_name in wb.sheetnames:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)  # Read each quarter sheet into a DataFrame
                    dataframes.append(df)
            if dataframes:
                combined_df = pd.concat(dataframes, ignore_index=True)  # Combine all quarter DataFrames into one large DataFrame
                # Group by Role and aggregate: sum numeric fields and take the first value for non-numeric fields (like Floor)
                agg_df = combined_df.groupby("Role", as_index=False).agg(
                    lambda x: x.sum() if pd.api.types.is_numeric_dtype(x) else x.iloc[0]
                )
                with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
                    agg_df.to_excel(writer, sheet_name="EoS", index=False)  # Save the aggregated results to the EoS sheet
        except Exception as e:
            messagebox.showerror("Error", f"Aggregation failed:\n{e}")  # If something goes wrong (e.g., file read error), show an error message

def update_shift_changes_summary(file_path):
    """
    Generate a summary DataFrame from the global shift_data dictionary and sort it by quarter (in logical order) and Role.
    This summary is written to the "Shift Changes" sheet for management to review all recorded data and changes.
    """
    rows = []
    for quarter, roles in shift_data.items():
        for role, data in roles.items():
            row = {"Quarter": quarter}  # Start a new row with the quarter name
            row.update(data)  # Add all data (metrics and role info) into the row dictionary
            rows.append(row)
    df = pd.DataFrame(rows) if rows else pd.DataFrame()  # Create a DataFrame of all data (or empty DataFrame if no data)
    # Define custom order for quarters to ensure sorting is SoS, Q1, Q2, Q3, EoS
    quarter_order = {"SoS": 1, "Q1": 2, "Q2": 3, "Q3": 4, "EoS": 5}
    if "Quarter" in df.columns:
        df["QuarterOrder"] = df["Quarter"].apply(lambda x: quarter_order.get(x, 99))
        df = df.sort_values(by=["QuarterOrder", "Role"])
        df = df.drop(columns=["QuarterOrder"])  # Remove the helper sorting column
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="Shift Changes", index=False)  # Write the sorted summary DataFrame to the "Shift Changes" sheet

def adjust_excel_columns(file_path):
    """Automatically adjust the width of columns in each sheet for better readability (so all content is visible)."""
    wb = load_workbook(file_path)  # Open the Excel workbook file
    for sheet in wb.sheetnames:  # Go through every sheet in the workbook
        ws = wb[sheet]
        for col in ws.columns:  # For each column in the current sheet
            max_length = 0
            column = col[0].column_letter  # Get the letter name of the column (like 'A', 'B', etc.)
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))  # Track the longest value length in this column
                except:
                    pass  # If we hit an unusual value, skip it
            ws.column_dimensions[column].width = max_length + 2  # Set column width to the longest value length + some padding
    wb.save(file_path)  # Save the workbook after adjusting column widths

# -------------------------------
# Delta Analysis Functions
# -------------------------------

def compute_deltas_between(q1, q2):
    """
    Compute the absolute and percent differences for each numeric metric for all roles
    that are common to both selected quarters (q1 and q2).
    Returns a summary text string and a pandas DataFrame of the differences.
    """
    rows = []
    summary_lines = []
    if q1 not in shift_data or q2 not in shift_data:
        return "One or both quarters are not available.", pd.DataFrame()  # If either quarter's data is missing, return a message and empty DataFrame
    roles1 = shift_data[q1]
    roles2 = shift_data[q2]
    common_roles = set(roles1.keys()).intersection(set(roles2.keys()))  # Roles present in both quarter datasets
    for role in common_roles:
        data1 = roles1[role]  # Data (all metrics) for this role in quarter q1
        data2 = roles2[role]  # Data for the same role in quarter q2
        for key in data1:  # For each metric in the role's data
            try:
                # Get old and new values for this metric, using 0 if a value is None or missing
                old_val = float(data1.get(key, 0)) if data1.get(key) is not None else 0
                new_val = float(data2.get(key, 0)) if data2.get(key) is not None else 0
            except:
                continue  # If the value cannot be converted to float (e.g., it's text), skip this metric
            diff = new_val - old_val  # Calculate the difference
            pct = (diff / old_val * 100) if old_val != 0 else 0  # Calculate percent change (avoid dividing by zero)
            rows.append({
                "Role": role,
                "Metric": key,
                "Old Value": old_val,
                "New Value": new_val,
                "Difference": diff,
                "Percent Change": pct
            })
            summary_lines.append(f"{role} - {key}: {old_val} -> {new_val} | Diff: {diff} | {pct:.1f}%")
    summary = "\n".join(summary_lines) if summary_lines else "No common numeric data found."
    df = pd.DataFrame(rows)
    return summary, df  # Return a text summary of differences and the DataFrame with detailed differences

# -------------------------------
# Delta Summary Window (Separate Window)
# -------------------------------

def open_delta_summary_window():
    """
    Opens a separate window that allows the user to select two quarters to compare,
    choose the type of graph (Bar or Line), select a metric, and view the delta analysis.
    A Help button is provided for additional instructions.
    """
    delta_win = tk.Toplevel(root)  # Create a new top-level window for the delta summary
    delta_win.title("Delta Summary Analysis")  # Set the title of the new window
    
    # Display instructions at the top of the window
    instructions = (
        "Instructions:\n"
        "1. Select two quarters to compare.\n"
        "2. Choose the graph type (Bar or Line).\n"
        "3. Click 'Generate Delta' to compute differences.\n"
        "4. Use the 'Select Metric' dropdown to choose a metric.\n"
        "5. Click 'Show Graph' to display a graph of the differences.\n"
        "6. Percent changes are shown along with absolute differences."
    )  # A multi-line string containing the usage instructions
    tk.Label(delta_win, text=instructions, justify="left", fg="blue").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # Quarter selection dropdowns
    tk.Label(delta_win, text="Select Quarter 1:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    delta_q1_var = tk.StringVar(value=QUARTERS[0])  # Variable for first quarter selection (default to first quarter)
    tk.OptionMenu(delta_win, delta_q1_var, *QUARTERS).grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(delta_win, text="Select Quarter 2:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    delta_q2_var = tk.StringVar(value=QUARTERS[1])  # Variable for second quarter selection (default to second quarter)
    tk.OptionMenu(delta_win, delta_q2_var, *QUARTERS).grid(row=2, column=1, padx=5, pady=5)
    
    # Graph type selection
    tk.Label(delta_win, text="Graph Type:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    graph_type_var = tk.StringVar(value="Bar")  # Variable for graph type (Bar or Line, default Bar)
    tk.OptionMenu(delta_win, graph_type_var, "Bar", "Line").grid(row=3, column=1, padx=5, pady=5)
    
    # Dropdown for selecting the metric (to be populated after generating delta data)
    tk.Label(delta_win, text="Select Metric:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    metric_var = tk.StringVar(value="")  # Variable for metric selection (initially empty)
    metric_menu = tk.OptionMenu(delta_win, metric_var, "")  # Dropdown menu for metrics (will be updated later)
    metric_menu.grid(row=4, column=1, padx=5, pady=5)
    
    # Text widget to display the delta summary (differences text)
    delta_text = tk.Text(delta_win, height=10, width=80)
    delta_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    delta_text.config(state="disabled")  # Make it read-only until we put text in it
    
    # Global variable to hold the computed delta DataFrame (so it can be accessed by graphing function)
    global delta_df_global
    delta_df_global = pd.DataFrame()
    
    def generate_delta():
        """Compute the delta differences and update the display."""
        summary, df = compute_deltas_between(delta_q1_var.get(), delta_q2_var.get())  # Compute differences between the two selected quarters
        global delta_df_global
        delta_df_global = df  # Store the DataFrame globally for use in the graph function
        delta_text.config(state="normal")  # Enable editing in the text widget to update content
        delta_text.delete("1.0", tk.END)  # Clear any existing text (from position 1.0 to end)
        delta_text.insert(tk.END, summary)  # Insert the summary text of differences
        delta_text.config(state="disabled")  # Make the text widget read-only again
        # Update the metric dropdown with the available metrics from the differences DataFrame
        metrics = df["Metric"].unique().tolist() if not df.empty else []
        if metrics:
            metric_var.set(metrics[0])  # Set the metric dropdown to the first metric as default
            menu = metric_menu["menu"]  # Access the menu object of the OptionMenu
            menu.delete(0, "end")  # Remove any existing menu items
            for m in metrics:
                menu.add_command(label=m, command=lambda value=m: metric_var.set(value))  # Add each metric as a selectable option
    
    def show_delta_graph():
        """Display a graph for the selected metric using the computed delta data."""
        if delta_df_global.empty:
            messagebox.showerror("Error", "Please generate delta data first.")  # Ensure data is generated before plotting
            return
        selected_metric = metric_var.get()  # Get the metric chosen by the user from the dropdown
        plot_df = delta_df_global[delta_df_global["Metric"] == selected_metric]  # Filter the DataFrame for just the selected metric
        if plot_df.empty:
            messagebox.showerror("Error", "No data for the selected metric.")  # If, for some reason, there's no data for that metric, show error
            return
        plt.figure(figsize=(6,4))
        if graph_type_var.get() == "Bar":  # If "Bar" type is selected
            plt.bar(plot_df["Role"], plot_df["Difference"])  # Create a bar chart: x-axis is Role, y-axis is Difference
        elif graph_type_var.get() == "Line":  # If "Line" type is selected
            plt.plot(plot_df["Role"], plot_df["Difference"], marker="o")  # Create a line plot with points marked
        plt.xlabel("Role")
        plt.ylabel("Difference")
        plt.title(f"Delta for {selected_metric}\n({delta_q1_var.get()} to {delta_q2_var.get()})")
        plt.xticks(rotation=45)  # Rotate x labels for readability if they're long
        plt.tight_layout()
        plt.show()
    
    def show_help():
        """Show a help message with instructions for using the Delta Summary window."""
        help_message = (
            "Delta Summary Help:\n"
            "- Select two quarters from the dropdown menus.\n"
            "- Choose a graph type (Bar or Line).\n"
            "- Click 'Generate Delta' to calculate differences between the two quarters.\n"
            "- The text box will display absolute differences and percent changes for each role and metric.\n"
            "- Use the 'Select Metric' dropdown to pick a specific metric, then click 'Show Graph' to view a graph of those differences."
        )
        messagebox.showinfo("Delta Summary Help", help_message)
    
    # Buttons to generate delta data, show the graph, and display help
    tk.Button(delta_win, text="Generate Delta", command=generate_delta).grid(row=6, column=0, padx=5, pady=5)
    tk.Button(delta_win, text="Show Graph", command=show_delta_graph).grid(row=6, column=1, padx=5, pady=5)
    tk.Button(delta_win, text="Help", command=show_help).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# -------------------------------
# Main GUI Functions for Data Entry
# -------------------------------

def validate_numeric(value):
    """Return True if the input is empty or entirely numeric (digits only)."""
    return value.strip() == "" or value.strip().isdigit()  # True if the string is blank or if it consists only of digits

def update_headcount_totals(*args):
    """Update the total headcounts for all RSP floors and for all non-RSP roles whenever an individual Headcount field changes."""
    global rsp_entries  # Use the global dictionary of RSP floor entries
    total_rsp = 0
    for floor in RSP_FLOORS:
        try:
            val = rsp_entries[floor]["Headcount"].get().strip()  # Get the headcount input for this floor and strip whitespace
            if val.isdigit():
                total_rsp += int(val)  # Add to RSP total if it's a valid number
        except KeyError:
            continue  # If for some reason the floor or field is missing, skip it
    rsp_headcount_total_var.set(str(total_rsp))  # Update the display variable for total RSP headcount
    
    total_non_rsp = 0
    try:
        val = dock_entries["Headcount"].get().strip()
        if val.isdigit():
            total_non_rsp += int(val)
    except KeyError:
        pass  # If dock headcount entry doesn't exist, ignore
    try:
        val = dmg_entries["Headcount"].get().strip()
        if val.isdigit():
            total_non_rsp += int(val)
    except KeyError:
        pass  # If damageland headcount entry doesn't exist, ignore
    for role in OTHER_ROLES:
        try:
            val = other_entries[role].get().strip()
            if val.isdigit():
                total_non_rsp += int(val)
        except KeyError:
            continue
    non_rsp_headcount_total_var.set(str(total_non_rsp))  # Update the display variable for total non-RSP headcount

def update_rsp_total(*args):
    """Update the total of 'Piles' for all RSP floors whenever any individual Piles field changes."""
    global rsp_entries
    total = 0
    for floor in RSP_FLOORS:
        try:
            val = rsp_entries[floor]["Piles"].get().strip()
            if val.isdigit():
                total += int(val)  # Add to total if value is numeric
        except KeyError:
            continue
    rsp_total_var.set(str(total))  # Update the display variable for total RSP Piles

def collect_data():
    """
    Collect all input data from the GUI and compile it into a list of dictionaries.
    Each dictionary in the list represents one record (row) of data to be saved.
    Returns the list of records.
    """
    records = []  # Will hold all data entries as dictionaries
    current_quarter = selected_quarter.get()  # Determine which quarter (SoS, Q1, Q2, Q3, or EoS) is currently selected
    
    # Collect data for each RSP floor
    for floor in RSP_FLOORS:
        rec = {"Quarter": current_quarter, "Role": f"RSP ({floor})", "Floor": floor}
        for metric in RSP_METRICS:
            val = rsp_entries[floor][metric].get().strip()  # Get the string from the entry field
            rec[metric] = int(val) if (val and validate_numeric(val)) else None  # If there's a value and it's numeric, convert to int; if empty, use None
        records.append(rec)
    # Calculate and add RSP Total for Piles
    total_piles = sum(int(rsp_entries[floor]["Piles"].get().strip()) for floor in RSP_FLOORS 
                      if rsp_entries[floor]["Piles"].get().strip().isdigit())
    records.append({"Quarter": current_quarter, "Role": "RSP (Total)", "Floor": "", "Piles": total_piles})
    # Add RSP Headcount Total record
    try:
        total_rsp_headcount = int(rsp_headcount_total_var.get())
    except:
        total_rsp_headcount = 0
    records.append({"Quarter": current_quarter, "Role": "RSP (Headcount Total)", "Floor": "", "Headcount": total_rsp_headcount})
    # Collect data for Dock
    rec = {"Quarter": current_quarter, "Role": "Dock", "Floor": ""}
    for metric in DOCK_METRICS:
        val = dock_entries[metric].get().strip()
        rec[metric] = int(val) if (val and validate_numeric(val)) else None
    records.append(rec)
    # Collect data for Damageland
    rec = {"Quarter": current_quarter, "Role": "Damageland", "Floor": ""}
    for metric in DAMAGELAND_METRICS:
        val = dmg_entries[metric].get().strip()
        rec[metric] = int(val) if (val and validate_numeric(val)) else None
    records.append(rec)
    # Collect data for Other Roles (Headcount only)
    for role in OTHER_ROLES:
        rec = {"Quarter": current_quarter, "Role": role, "Floor": ""}
        val = other_entries[role].get().strip()
        rec["Headcount"] = int(val) if (val and validate_numeric(val)) else None
        records.append(rec)
    # Add Non-RSP Headcount Total record
    try:
        total_non_rsp_headcount = int(non_rsp_headcount_total_var.get())
    except:
        total_non_rsp_headcount = 0
    records.append({"Quarter": current_quarter, "Role": "Non-RSP (Headcount Total)", "Floor": "", "Headcount": total_non_rsp_headcount})
    return records

def clear_fields():
    """Clear all input fields in the GUI after data submission (reset the form for the next entry)."""
    for floor in RSP_FLOORS:
        for metric in RSP_METRICS:
            rsp_entries[floor][metric].set("")  # Empty all RSP floor fields
    for metric in DOCK_METRICS:
        dock_entries[metric].set("")  # Empty Dock fields
    for metric in DAMAGELAND_METRICS:
        dmg_entries[metric].set("")  # Empty Damageland fields
    for role in OTHER_ROLES:
        other_entries[role].set("")  # Empty fields for other roles
    rsp_total_var.set("0")  # Reset total displays back to "0"
    rsp_headcount_total_var.set("0")
    non_rsp_headcount_total_var.set("0")

def submit_data():
    """
    When the user clicks "Submit", this function:
      - Collects data from the GUI.
      - Creates the Excel workbook if it doesn't exist.
      - Saves the current quarter's data to the Excel file.
      - Updates the EoS sheet appropriately (if EoS quarter data is submitted, it directly mirrors that submission).
      - Updates the Shift Changes sheet with an up-to-date summary of all data.
      - Adjusts column widths in the Excel file for readability.
    """
    records = collect_data()  # Gather all the input data from the form into a list of records
    if records is None:
        return  # If collecting data failed or was canceled, stop here
    file_path = get_excel_file_path(shift_date_var.get(), shift_type_var.get())  # Determine the file path for the Excel file (based on date and type)
    if not os.path.exists(file_path):
        create_new_workbook(file_path)  # If the file doesn't exist yet, create a new workbook with all sheets
    diff_entries = []
    try:
        old_df = pd.read_excel(file_path, sheet_name=selected_quarter.get())  # Read existing data from the Excel sheet of the current quarter (if any)
        new_df = pd.DataFrame(records)  # Convert new records to a DataFrame for comparison
        diff_entries = compute_differences(old_df, new_df)  # Compute differences between old and new data (function may not be implemented in this code version)
    except Exception as e:
        print(f"Warning: Could not compute differences: {e}")  # If difference computation fails, just warn (not critical)
    try:
        save_quarter_to_excel(selected_quarter.get(), records, file_path)  # Save the new quarter's data into the Excel file
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data to Excel:\n{e}")
        return
    # Update the EoS sheet:
    # If the current quarter is EoS, simply update the EoS sheet with the submitted data.
    # Otherwise, aggregate data from SoS, Q1, Q2, and Q3 to update EoS.
    aggregate_data(file_path, current_quarter=selected_quarter.get())
    update_shift_changes_summary(file_path)
    adjust_excel_columns(file_path)
    messagebox.showinfo("Success", f"Data for {selected_quarter.get()} saved successfully!")
    load_data_from_json()  # Refresh the in-memory data from the JSON file (now including the latest submission)
    clear_fields()  # Clear the form fields to prepare for the next entry

def show_graphs():
    """Display a simple trend line graph for RSP Total Piles over the quarters that have data."""
    available_quarters = [q for q in QUARTERS if q in shift_data and any("RSP (Total)" in shift_data[q])]
    if not available_quarters:
        return  # If there's no data yet, exit without showing anything
    x = list(range(len(available_quarters)))  # X-axis values as indices 0,1,2,... for each available quarter
    y = []
    for q in available_quarters:
        try:
            val = int(shift_data[q]["RSP (Total)"].get("Piles", 0))
        except Exception:
            val = 0
        y.append(val)  # Append the Piles total for that quarter (or 0 if missing)
    plt.figure(figsize=(6,4))
    plt.plot(x, y, marker="o", linestyle="-", color="blue")  # Plot the points with a line connecting them
    plt.xticks(x, available_quarters)  # Label the x-axis ticks with quarter names
    plt.xlabel("Quarter")
    plt.ylabel("RSP Total Piles")
    plt.title("Trend of RSP Total Piles Over Quarters")
    plt.tight_layout()
    plt.show()

# -------------------------------
# Main GUI Setup with Scrollbar
# -------------------------------
# The following section builds the Graphical User Interface (GUI) for the application.

root = tk.Tk()  # Create the main application window
root.title("Shift Logger for Problem Solve Department")  # Set the window title

# Create a main frame with a canvas and vertical scrollbar for all content (to allow scrolling if content is long)
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Top Frame: Shift Info and Import Files (inputs for shift type, date, and import button)
top_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
top_frame.pack(fill="x")
tk.Label(top_frame, text="Shift Type (Day/Night):").grid(row=0, column=0, sticky="w")
shift_type_var = tk.StringVar(value="Day")  # Default shift type is "Day"
tk.Entry(top_frame, textvariable=shift_type_var, width=10).grid(row=0, column=1, padx=5)
tk.Label(top_frame, text="Shift Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w")
shift_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))  # Default to today's date
tk.Entry(top_frame, textvariable=shift_date_var, width=12).grid(row=0, column=3, padx=5)
def on_import_files():
    import_files()  # Call the import_files function when button is pressed
tk.Button(top_frame, text="Import Files", command=on_import_files, bg="lightgreen").grid(row=0, column=4, padx=10)
tk.Button(top_frame, text="Open Delta Summary", command=open_delta_summary_window, bg="orange").grid(row=0, column=5, padx=10)

# Middle Frame: Quarter Selection (dropdown menu to choose which quarter the data belongs to)
mid_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
mid_frame.pack(fill="x")
tk.Label(mid_frame, text="Select Quarter:").grid(row=0, column=0, sticky="w")
selected_quarter = tk.StringVar(value=QUARTERS[0])  # Default selected quarter is the first (SoS)
tk.OptionMenu(mid_frame, selected_quarter, *QUARTERS).grid(row=0, column=1, padx=5)

# Main Data Entry Frame (contains all input sections for RSP, Dock, Damageland, Other roles)
data_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
data_frame.pack(fill="both", expand=True)

# --- RSP Floors Data Entry ---
tk.Label(data_frame, text="RSP Floors (Enter counts below)", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=7, pady=5)
rsp_entries = {}  # Dictionary to store StringVar for each metric of each RSP floor
header = ["Floor"] + RSP_METRICS
for col, h in enumerate(header):
    tk.Label(data_frame, text=h, font=("Arial", 10, "underline")).grid(row=1, column=col, padx=3, pady=3)
row_idx = 2
for floor in RSP_FLOORS:
    rsp_entries[floor] = {}
    tk.Label(data_frame, text=f"RSP {floor}:").grid(row=row_idx, column=0, sticky="e", padx=3)
    for j, metric in enumerate(RSP_METRICS, start=1):
        var = tk.StringVar()
        rsp_entries[floor][metric] = var  # Store the variable in the dictionary for later reference
        tk.Entry(data_frame, textvariable=var, width=8).grid(row=row_idx, column=j, padx=3, pady=2)
        if metric == "Headcount":
            var.trace_add("write", update_headcount_totals)  # When headcount changes, update totals
        elif metric == "Piles":
            var.trace_add("write", update_rsp_total)  # When piles changes, update the total piles
    row_idx += 1

# Display RSP Totals (read-only fields for total Piles and headcounts)
tk.Label(data_frame, text="RSP Total (Piles):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
rsp_total_var = tk.StringVar(value="0")
tk.Entry(data_frame, textvariable=rsp_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
row_idx += 1

tk.Label(data_frame, text="RSP Total (Headcount):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
rsp_headcount_total_var = tk.StringVar(value="0")
tk.Entry(data_frame, textvariable=rsp_headcount_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
row_idx += 1

tk.Label(data_frame, text="Non-RSP Total (Headcount):", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="e", padx=3)
non_rsp_headcount_total_var = tk.StringVar(value="0")
tk.Entry(data_frame, textvariable=non_rsp_headcount_total_var, width=8, state="readonly").grid(row=row_idx, column=1, padx=3, pady=2)
row_idx += 2  # Add an extra blank row space after totals

# --- Dock Data Entry ---
tk.Label(data_frame, text="Dock (Enter counts)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=8, pady=5)
row_idx += 1
dock_entries = {}  # Dictionary for Dock metrics entry variables
header = ["Role"] + DOCK_METRICS
for col, h in enumerate(header):
    tk.Label(data_frame, text=h, font=("Arial", 10, "underline")).grid(row=row_idx, column=col, padx=3, pady=3)
row_idx += 1
tk.Label(data_frame, text="Dock:").grid(row=row_idx, column=0, sticky="e", padx=3)
for j, metric in enumerate(DOCK_METRICS, start=1):
    var = tk.StringVar()
    dock_entries[metric] = var
    tk.Entry(data_frame, textvariable=var, width=8).grid(row=row_idx, column=j, padx=3, pady=2)
    if metric == "Headcount":
        var.trace_add("write", update_headcount_totals)
row_idx += 2

# --- Damageland Data Entry ---
tk.Label(data_frame, text="Damageland (Enter counts)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=6, pady=5)
row_idx += 1
dmg_entries = {}  # Dictionary for Damageland metrics entry variables
header = ["Role"] + DAMAGELAND_METRICS
for col, h in enumerate(header):
    tk.Label(data_frame, text=h, font=("Arial", 10, "underline")).grid(row=row_idx, column=col, padx=3, pady=3)
row_idx += 1
tk.Label(data_frame, text="Damageland:").grid(row=row_idx, column=0, sticky="e", padx=3)
for j, metric in enumerate(DAMAGELAND_METRICS, start=1):
    var = tk.StringVar()
    dmg_entries[metric] = var
    tk.Entry(data_frame, textvariable=var, width=8).grid(row=row_idx, column=j, padx=3, pady=2)
    if metric == "Headcount":
        var.trace_add("write", update_headcount_totals)
row_idx += 2

# --- Other Roles Data Entry (Headcount only) ---
tk.Label(data_frame, text="Other Roles (Headcount Only)", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, columnspan=3, pady=5)
row_idx += 1
other_entries = {}  # Dictionary for Other roles (each only has headcount entry)
for role in OTHER_ROLES:
    tk.Label(data_frame, text=f"{role}:").grid(row=row_idx, column=0, sticky="e", padx=3)
    var = tk.StringVar()
    other_entries[role] = var
    tk.Entry(data_frame, textvariable=var, width=8).grid(row=row_idx, column=1, padx=3, pady=2)
    var.trace_add("write", update_headcount_totals)
    row_idx += 1

# Status Label and Submit Button at the bottom
status_label = tk.Label(scrollable_frame, text="", fg="blue", font=("Arial", 10))
status_label.pack(pady=5)  # This label could be used to show status messages (currently blank)
submit_btn = tk.Button(scrollable_frame, text="Submit", command=submit_data, bg="lightblue", font=("Arial", 12))
submit_btn.pack(pady=10)  # When clicked, triggers the submit_data function

root.mainloop()  # Start the Tkinter event loop (this displays the window and keeps the app running)