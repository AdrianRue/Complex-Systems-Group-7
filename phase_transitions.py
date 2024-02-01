from CellularAutomaton import CellularAutomaton
import numpy as np
import matplotlib.pyplot as plt


def simulate(N, probs_gas, frames=1000, runs=10, proto_size=25, star_size=100, steps_dissipating=50):
    results = []
    for prob_gas in probs_gas:
        print('Simulating for prob_gas =', prob_gas)
        emergence = [prob_gas, 0, 0]
        for i in range(runs):
            print('Run', i+1, 'of', runs)
            p = [1 - prob_gas, prob_gas]

            # Initialize the cellular automaton
            automaton = CellularAutomaton(N, p, proto_size, star_size, steps_dissipating)

            proto = False
            star = False
            for j in range(frames):
                states = automaton.update(j)

                if 2 in states:
                    proto = True
                if 3 in states:
                    star = True
                    break

            # Add to emergence
            emergence[1] += int(proto)
            emergence[2] += int(star)

        # Divide by runs
        emergence[1] /= runs
        emergence[2] /= runs

        # Add to results
        results.append(emergence)

        print(emergence)
        print('')

    results = np.array(results)
    # Save results
    np.savetxt('results/emergence.txt', results, delimiter=',')

    # Plot results
    plot_transitions(results)

def plot_transitions(data):
    # Create figure
    fig, ax = plt.subplots(2)

    # Titles
    titles = ['Emergence of proto-star', 'Emergence of star']

    for i in range(2):
        # Plot
        ax[i].plot(data[:, 0], data[:, i+1])

        # Labels and title
        ax[i].set_title(titles[i])
        ax[i].set_xlabel('Gas density')
        ax[i].set_ylabel('Probability of emergence')

        # Grid
        ax[i].grid()

    # Tight layout
    fig.tight_layout()

    # Show figure
    plt.show()

    return fig, ax

def load_results(file, save=None):
    # Load results
    results = np.loadtxt(file, delimiter=',')

    # Plot
    fig, ax = plot_transitions(results)

    if save:
        fig.savefig(save, dpi=300)

if __name__ == '__main__':
    # N = 100
    # probs_gas = np.linspace(0.02, 0.2, 10, endpoint=True)
    # simulate(N, probs_gas)
    load_results('results/emergence.txt', 'figures/emergence.png')










