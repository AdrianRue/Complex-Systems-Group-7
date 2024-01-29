import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

from CellularAutomaton import CellularAutomaton

# Initialize the argument parser
parser = argparse.ArgumentParser(description='2D Cellular Automaton Star Formation Simulation', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--N', type=int, default=100, help='Grid size')
parser.add_argument('--prob_gas', type=float, default=0.15, help='Probability of gas')
parser.add_argument('--proto_size', type=int, default=35, help='Proto size')
parser.add_argument('--star_size', type=int, default=200, help='Star size')

# Parse the arguments
args = parser.parse_args()

def simulate(N, prob_gas, proto_size, star_size):
    p = [1-prob_gas, prob_gas]

    # Initialize the cellular automaton
    automaton = CellularAutomaton(N, p, proto_size, star_size)

    # Define colors for each state
    colors = {0: 'white',  # Color for state 0
            1: 'blue',   # Color for state 1
            2: 'red',    # Color for state 2
            3: 'green'}  # Color for state 3

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
    # Call the simulate function with arguments from the command line
    simulate(args.N, args.prob_gas, args.proto_size, args.star_size)