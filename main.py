import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from scipy.stats import powerlaw

from CellularAutomaton import CellularAutomaton

# Initialize the argument parser
parser = argparse.ArgumentParser(description='2D Cellular Automaton Star Formation Simulation', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--N', type=int, default=150, help='Grid size')
parser.add_argument('--prob_gas', type=float, default=0.15, help='Probability of gas')
parser.add_argument('--proto_size', type=int, default=35, help='Proto size')
parser.add_argument('--star_size', type=int, default=200, help='Star size')

# Parse the arguments
args = parser.parse_args()

def simulate(N, prob_gas, proto_size, star_size):
    assert isinstance(N, int) and N > 0, "Grid size N must be a positive integer."
    assert isinstance(prob_gas, float) and 0 <= prob_gas <= 1, "Probability of gas must be a float between 0 and 1."
    assert isinstance(proto_size, int) and 0 < proto_size <= N*N, "Proto size must be a positive integer and less than or equal to N."
    assert isinstance(star_size, int) and 0 < star_size <= N*N, "Star size must be a positive integer and less than or equal to N."

    p = [1-prob_gas, prob_gas]

    # Initialize the cellular automaton
    automaton = CellularAutomaton(N, p, proto_size, star_size)

    global counts
    time_step_counter = 0
    counts = {1: [], 2: [], 3: []}  # Dictionary of lists for each state

    # Define colors for each state
    colors = {0: 'white',  # Color for state 0
            1: 'green',   # Color for state 1
            2: 'orange',    # Color for state 2
            3: 'yellow',
            4: 'blue'}  # Color for state 3

    # Create a color map from the defined colors
    cmap = mcolors.ListedColormap([colors[i] for i in range(len(colors))])

    # Set up the figure for visualization
    fig, ax = plt.subplots()
    mat = ax.matshow(automaton.get_grid_states(), cmap=cmap, vmin=0, vmax=len(colors))

    # Update function for the animation
    def update(frame):
        nonlocal time_step_counter
        if time_step_counter >= 400:
            plt.close()  # Closes the plot and ends the animation
            return
        
        counts[1].append(sum(agent.state == 1 for row in automaton.grid for agent in row))
        counts[2].append(sum(agent.state == 2 for row in automaton.grid for agent in row))
        counts[3].append(sum(agent.state == 3 for row in automaton.grid for agent in row))

        mat.set_data(automaton.update(frame))

        time_step_counter += 1
        return [mat]

    ani = animation.FuncAnimation(fig, update, interval=1/120, save_count=50)
    plt.show()


def check_powerlaw(prob_gas):
    data = counts[1]

    # Prepare data for analysis
    hist, bin_edges = np.histogram(data, bins='auto', density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Fit the data to a power-law distribution
    a, loc, scale = powerlaw.fit(data)


    # Plot the data on a log-log scale
    plt.loglog(bin_centers, hist, 'o', label='bin_centers')
    plt.loglog(bin_centers, powerlaw.pdf(bin_centers, a, loc, scale), '-', label='powerlaw fit')
    plt.xlabel('Count')
    plt.ylabel('Probability Density')
    plt.title(f'Log-Log Plot with Power Law Fit (Gas Density {prob_gas})')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # probs_gas = np.arange(0.01, 0.21, 0.05)
    probs_gas = [0.15]

    for prob_gas in probs_gas:
        # Call the simulate function with arguments from the command line
        simulate(args.N, args.prob_gas, args.proto_size, args.star_size)
        check_powerlaw(prob_gas)

        labels = {1: "gas", 2: "Protostar", 3: "Star"}

        # Plotting the time series data     
        time_steps = range(len(counts[1]))
        plt.figure()
        for state in counts:
            plt.plot(time_steps, counts[state], label=f'State {labels[state]}')
        plt.xlabel('Time Step')
        plt.ylabel('Count')
        plt.title('State Counts Over Time')
        plt.legend()
        plt.xlim(left=150)
        plt.show()