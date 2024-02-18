import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def create_chart(results, chart_window):
    # Extract relevant data for plotting
    percentages = [float(result[2].strip('%')) / 100 for result in results]
    accumulative_values = [float(result[-1].replace('$', '').replace(',', '')) for result in results]

    # Extract unique simulation sets
    unique_sets = list(set(result[0].split('_')[1] for result in results))

    # Define colors for each simulation set
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_sets)))

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, set_id in enumerate(unique_sets):
        set_indices = [j for j, result in enumerate(results) if result[0].split('_')[1] == set_id]
        
        # Extract accumulated values for each set
        accumulated_values_set = [float(result[-3].replace('$', '').replace(',', '')) for result in results]
        
        # Plot using accumulated values
        ax.scatter([percentages[idx] for idx in set_indices], [accumulated_values_set[idx] for idx in set_indices],
                marker='x', color=colors[i])

        # Add numeric values on the right side of "x" markers
        for idx in set_indices:
            value = accumulated_values_set[idx]
            ax.text(percentages[idx], value, f'${int(value):,}', fontsize=8, va='center', ha='left')


    # Customize the plot
    ax.set_title('Simulation Results Chart')
    ax.set_xlabel('Percentage')
    ax.set_ylabel('Accumulative Value')
    ax.set_ylim(0, 100000)  # Set y-axis limit
    ax.legend([f'{int(result[4])} @ ${float(result[1].replace("$", "")):.2f} ({percent:.2%})' for set_id, percent, result in zip(unique_sets, percentages, results)], loc='upper right', bbox_to_anchor=(0.98, 0.98), prop={'size': 8})
    ax.grid(True)
    
    # Embed the plot in the chart_window
    chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
    chart_canvas_widget = chart_canvas.get_tk_widget()
    chart_canvas_widget.pack()
    chart_canvas.draw()

    # Show the chart_window
    chart_window.mainloop()

# Example usage
if __name__ == "__main__":
    # Replace the example_data with your actual simulation results
    example_data = [
        ("735_50@20", "$20.00", "50%", "$10000.00", "500", "235", "$10000.00", "$23500.00", "$33500.00"),
        ("735_60@20", "$20.00", "60%", "$12000.00", "600", "135", "$12000.00", "$13500.00", "$25500.00"),
        # Add more simulation results as needed
    ]

    # For testing purposes, create_chart is called without opening a separate chart window
    create_chart(example_data, tk.Tk())
