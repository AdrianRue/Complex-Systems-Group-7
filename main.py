import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

from CellularAutomaton import CellularAutomaton

def simulate(N, prob_gas, proto_size, star_size):
    p = [1-prob_gas, prob_gas]

    # Initialize the cellular automaton
    automaton = CellularAutomaton(N, p, proto_size, star_size)

    # Define colors for each state
    colors = {0: 'white',  # Color for state 0
            1: 'blue',   # Color for state 1
            2: 'red',    # Color for state 2
            3: 'green',
            4: 'pink'}  # Color for state 3

    # Create a color map from the defined colors
    cmap = mcolors.ListedColormap([colors[i] for i in range(len(colors))])

    # Set up the figure for visualization
    fig, ax = plt.subplots()
    mat = ax.matshow(automaton.get_grid_states(), cmap=cmap, vmin=0, vmax=len(colors))

    # Update function for the animation
    def update(frame):
        mat.set_data(automaton.update(frame))
        return [mat]

    ani = animation.FuncAnimation(fig, update, interval=1/120, save_count=50)
    plt.show()


if __name__ == "__main__":
    N = 100             # Grid size
    p = 0.15            # Prob of cell being gas
    proto_size = 35     # Number of adjacent gas cells needed for a protostar 
    star_size = 200     # Number of adjacent protostar cells needed for a protostar 

    simulate(N, p, proto_size, star_size)