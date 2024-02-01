import argparse, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from scipy.stats import powerlaw, expon, pearsonr

from CellularAutomaton import CellularAutomaton

# Initialize the argument parser
parser = argparse.ArgumentParser(description='2D Cellular Automaton Star Formation Simulation', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--N', type=int, default=100, help='Grid size')
parser.add_argument('--prob_gas', type=float, default=0.1, help='Probability of cell being a gas particle')
parser.add_argument('--proto_size', type=int, default=20, help='Size needed to form proto star')
parser.add_argument('--star_size', type=int, default=100, help='Size needed to form star')
parser.add_argument('--steps_dissipating', type=int, default=50, help='Steps dissipation')

# Parse the arguments
args = parser.parse_args()

def simulate(N, prob_gas, proto_size, star_size, steps_dissipating):
    assert isinstance(N, int) and N > 0, "Grid size N must be a positive integer."
    assert isinstance(prob_gas, float) and 0 <= prob_gas <= 1, "Probability of gas must be a float between 0 and 1."
    assert isinstance(proto_size, int) and 0 < proto_size <= N*N, "Proto size must be a positive integer and less than or equal to N."
    assert isinstance(star_size, int) and 0 < star_size <= N*N, "Star size must be a positive integer and less than or equal to N."
    assert isinstance(steps_dissipating, int) and 0 < steps_dissipating, "Steps dissipating must be a positive integer."
    

    p = [1-prob_gas, prob_gas]

    # Initialize the cellular automaton
    automaton = CellularAutomaton(N, p, proto_size, star_size, steps_dissipating)

    global counts
    global star_formations
    time_step_counter = 0
    state_3_groups = set()
    star_formation_counter = 0

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
        nonlocal time_step_counter, state_3_groups, star_formation_counter
        # print(time_step_counter)
        if time_step_counter >= 1000:
            star_formations.append(star_formation_counter)
            plt.close()  # Closes the plot and ends the animation
            return
                
        current_state_3_groups = {group for group in automaton.groups if group.state == 3}
        new_state_3_groups = current_state_3_groups - state_3_groups
        if new_state_3_groups:
            # For each new group of state 3, update the counter
            star_formation_counter += len(new_state_3_groups)
        
        # Update the tracking set to the current set of groups in state 3
        state_3_groups = current_state_3_groups

        counts[1].append(sum(agent.state == 1 for row in automaton.grid for agent in row))
        counts[2].append(sum(agent.state == 2 for row in automaton.grid for agent in row))
        counts[3].append(sum(agent.state == 3 for row in automaton.grid for agent in row))

        mat.set_data(automaton.update(frame))

        time_step_counter += 1
        return [mat]

    ani = animation.FuncAnimation(fig, update, interval=1/120, save_count=1000)
    
    # To save the animation using Pillow as a gif
    ani.save(f'results/gifs/density_{prob_gas}.gif', writer=animation.PillowWriter(fps=15))
    # plt.show()

def check_dist(prob_gas):
    data = counts[3]

    # Prepare data for analysis
    hist, bin_edges = np.histogram(data, bins='auto', density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Fit the data to a power-law distribution
    a, loc, scale = powerlaw.fit(data)

    # Fit the data to an exponential distribution
    param = expon.fit(data, floc=0)
    exponential_pdf = expon.pdf(bin_centers, *param)

    # Plot the data on a log-log scale
    plt.loglog(bin_centers, hist, 'o', label='bin_centers')
    plt.loglog(bin_centers, powerlaw.pdf(bin_centers, a, loc, scale), '-', label='powerlaw fit')    # Plot the powerlaw fit
    plt.loglog(bin_centers, exponential_pdf, '-', label='Exponential fit')                          # Plot the exponential fit
    plt.xlabel('Count')
    plt.ylabel('Probability Density')
    plt.title(f'Log-Log Plot with fit (Gas Density {prob_gas})')
    plt.legend()
    plt.savefig(f'results/fit_checks/dist_{prob_gas}.png')
    plt.close()


def check_pearson(probs_gas):
    stars_formed = np.array(star_formations)
    print(probs_gas, stars_formed)
    correlation_coefficient, p_value = pearsonr(probs_gas, stars_formed)
    print(correlation_coefficient, p_value)


if __name__ == "__main__":
    probs_gas = np.arange(0.02, 0.21, 0.045)
    # probs_gas = [0.20]
    print(probs_gas)
    star_formations = []
    for prob_gas in probs_gas:
        # Call the simulate function with arguments from the command line
        simulate(args.N, prob_gas, args.proto_size, args.star_size, args.steps_dissipating)
        check_dist(prob_gas)
    
    check_pearson(probs_gas)
