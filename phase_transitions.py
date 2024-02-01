from CellularAutomaton import CellularAutomaton
import numpy as np
import matplotlib.pyplot as plt


def simulate(N, probs_gas, frames=2000, runs=5, proto_size=35, star_size=200, steps_dissipating=50):
    results = []
    for prob_gas in probs_gas:
        emergence = [prob_gas, 0, 0]
        for i in range(runs):
            p = [1 - prob_gas, prob_gas]

            # Initialize the cellular automaton
            automaton = CellularAutomaton(N, p, proto_size, star_size, steps_dissipating)

            proto = False
            star = False
            for i in range(frames):
                states = automaton.update(i)

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

    results = np.array(results)
    # Save results
    np.savetxt('results/emergence.txt', results, delimiter=',')

    # Create figure
    fig, ax = plt.subplots(2)

    # First plot
    ax[0].plot(results[:, 0], results[:, 1])
    ax[0].set_title('Emergence of proto-star')

    # Second plot
    ax[1].plot(results[:, 0], results[:, 2])
    ax[1].set_title('Emergence of star')

    fig.tight_layout()

    # Show figure
    plt.show()

if __name__ == '__main__':
    N = 100
    probs_gas = np.arange(0.05, 0.55, 0.05)
    simulate(N, probs_gas)









