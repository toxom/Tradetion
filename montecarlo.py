import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog
from chart import create_chart
import random

class MCSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Monte Carlo Simulator")

        # Initial values
        self.initial_tokens = tk.IntVar(value=735)
        self.initial_valuation_range = tk.StringVar(value="18.67-20.67")  # Initial valuation range as a string "min-max"

        # Selling scenario
        self.sell_percentage = tk.IntVar(value=50)
        self.sell_valuation = tk.DoubleVar(value=20.0)

        # Simulation parameters
        self.gap = tk.IntVar(value=5)
        self.max_calculations = tk.IntVar(value=3)

        # Variable to store simulation results
        self.simulation_results = []

        # UI elements

        # Input section
        input_frame = tk.Frame(master)
        input_frame.grid(row=1, column=0, columnspan=9, pady=5, sticky="w")

        self.tokens_label = tk.Label(input_frame, text="Number of Tokens:")
        self.tokens_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.tokens_entry = tk.Entry(input_frame, textvariable=self.initial_tokens, width=5)
        self.tokens_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Initial valuation range inputs
        self.valuation_range_label = tk.Label(input_frame, text="Initial Valuation Range:")
        self.valuation_range_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.valuation_range_entry = tk.Entry(input_frame, textvariable=self.initial_valuation_range, width=12)
        self.valuation_range_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Remove percentage input
        self.scenario_percentage_label = tk.Label(input_frame, text="Percentage:")
        self.scenario_percentage_label.grid_forget()
        self.scenario_percentage_entry = tk.Entry(input_frame, textvariable=self.sell_percentage, width=5)
        self.scenario_percentage_entry.grid_forget()

        self.max_calculations_label = tk.Label(input_frame, text="Max Calculations:")
        self.max_calculations_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.max_calculations_entry = tk.Entry(input_frame, textvariable=self.max_calculations, width=5)
        self.max_calculations_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        self.gap_label = tk.Label(input_frame, text="Sell Gap:")
        self.gap_label.grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.gap_entry = tk.Entry(input_frame, textvariable=self.gap, width=5)
        self.gap_entry.grid(row=0, column=7, padx=5, pady=5, sticky="w")

        # Buttons
        self.run_simulation_button = tk.Button(master, text="Run Simulation", width=15, command=self.run_simulation)
        self.run_simulation_button.grid(row=0, column=3, pady=5, padx=5, sticky="w")

        self.export_button = tk.Button(master, text="Export to CSV", width=15, command=self.export_to_csv)
        self.export_button.grid(row=0, column=4, pady=5, padx=5, sticky="w")

        self.reset_button = tk.Button(master, text="Reset Inputs", width=15, command=self.reset_inputs)
        self.reset_button.grid(row=0, column=5, pady=5, padx=5, sticky="w")

        self.quit_button = tk.Button(master, text="Quit", width=15, command=master.quit)
        self.quit_button.grid(row=0, column=6, pady=5, padx=5, sticky="w")

        # Button to open the chart window
        self.create_chart_button = tk.Button(master, text="Create Chart", width=15, command=self.open_chart_window)
        self.create_chart_button.grid(row=0, column=7, pady=5, padx=5, sticky="w")

        # Results tree
        self.results_tree = ttk.Treeview(master, columns=("ID", "Valuation", "Sold Percentage", "Sold Value", "Sold Tokens", "Remaining Tokens", "Accumulative Value", "Left Token Stack Value", "Total Value"))
        self.results_tree.column("#0", width=60)
        self.results_tree.heading("#0", text="#")
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("Valuation", text="Valuation")
        self.results_tree.heading("Sold Percentage", text="Sold %")
        self.results_tree.heading("Sold Value", text="Sold $")
        self.results_tree.heading("Sold Tokens", text="Sold #")
        self.results_tree.heading("Remaining Tokens", text="Left #")
        self.results_tree.heading("Accumulative Value", text="Profit")
        self.results_tree.heading("Left Token Stack Value", text="Prospect")
        self.results_tree.heading("Total Value", text="Portfolio")
        self.results_tree.grid(row=4, column=0, rowspan=8, columnspan=9, padx=5, pady=5, sticky="nsew")

        # Set default column widths
        self.results_tree.column("ID", width=80)
        for col in self.results_tree["columns"][0:]:
            self.results_tree.column(col, width=80)

        # Configure column weights to make the table flexible
        for i in range(9):
            self.master.grid_columnconfigure(i, weight=1)
        self.master.grid_rowconfigure(4, weight=1)

    def run_simulation(self):
        num_simulations = 10  # You can adjust the number of simulations

        for simulation in range(num_simulations):
            current_iteration = 1
            initial_valuation_min, initial_valuation_max = map(float, self.initial_valuation_range.get().split('-'))
            current_valuation = random.uniform(initial_valuation_min, initial_valuation_max)
            current_tokens = self.initial_tokens.get()
            accumulative_value = 0

            max_calculations = self.max_calculations.get()

            # Sample input parameters randomly
            sold_percentage = random.uniform(0, 1)
            sell_valuation = round(random.uniform(float(current_valuation), float(current_valuation) + self.gap.get()), 2)
            sell_gap = self.gap.get()

            for _ in range(max_calculations):
                total_value = current_tokens * current_valuation

                sold_tokens = current_tokens * sold_percentage
                sold_value = sold_tokens * sell_valuation
                remaining_tokens = current_tokens - sold_tokens
                remaining_value = remaining_tokens * current_valuation

                # Update accumulative value
                accumulative_value += sold_value

                # Build ID for the simulation
                simulation_id = f"{current_tokens}_{int(sold_percentage * 100)}@{sell_valuation}"

                # Format percentage to display with two decimals
                formatted_percentage = f"{sold_percentage:.2%}"

                # Update the results tree
                self.results_tree.insert("", tk.END, text=str(current_iteration),
                                         values=(simulation_id, f"${current_valuation:.2f}", formatted_percentage,
                                                 f"${sold_value:.2f}", f"{int(sold_tokens)}", f"{int(remaining_tokens)}",
                                                 f"${accumulative_value:.2f}", f"${remaining_value:.2f}",
                                                 f"${accumulative_value + remaining_value:.2f}"))

                current_iteration += 1
                current_valuation += sell_gap
                current_tokens = int(remaining_tokens)

                # Append the simulation result to the list
                self.simulation_results.append((simulation_id, f"${current_valuation:.2f}", formatted_percentage,
                                                f"${sold_value:.2f}", f"{int(sold_tokens)}", f"{int(remaining_tokens)}",
                                                f"${accumulative_value:.2f}", f"${remaining_value:.2f}",
                                                f"${accumulative_value + remaining_value:.2f}"))

    def open_chart_window(self):
        # Create a new window for the chart
        chart_window = tk.Toplevel(self.master)
        chart_window.title("Simulation Results Chart")

        # Call the create_chart function from chart.py with the dynamically obtained results
        create_chart(self.simulation_results, chart_window)

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Iteration", "ID", "Valuation", "Sold Percentage", "Sold Value", "Sold Tokens", "Remaining Tokens", "Accumulative Value", "Left Token Stack Value", "Total Value"])
                for i in range(len(self.results_tree.get_children())):
                    values = self.results_tree.item(i, 'values')
                    writer.writerow([i + 1] + values)

    def reset_inputs(self):
        self.initial_tokens.set(735)
        self.initial_valuation_range.set("18.67-20.67")
        self.sell_percentage.set(50)
        self.max_calculations.set(3)
        self.gap.set(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MCSimulator(root)
    root.mainloop()
