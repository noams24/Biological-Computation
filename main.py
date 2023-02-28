from app import App
from genetic_algo import *
import pandas as pd


def main():
    population = create_random_population()
    best_chromosome = population[-1]
    no_improvement_counter = 0

    for i in range(MAX_GENERATIONS):
        print(f'generation: {i}')
        population = next_generation(population)

        if best_chromosome[1] < population[-1][1]:
            best_chromosome = population[-1]
            no_improvement_counter = 0
            print(f'found new temporary solution: {best_chromosome[0]}')
        else:
            no_improvement_counter += 1
            if no_improvement_counter == MAX_GENERATIONS_WITHOUT_IMPROVEMENT:
                break

    # summary:

    print(f'\nbest "Methuselah":{best_chromosome[0]}')
    print(f'fitness:{best_chromosome[1]}')
    print(f'game of life iterations: {best_chromosome[2]}')

    # launch app:
    App(MAT_SIZE, CELL_CIZE, best_chromosome[0], best_chromosome[2])

    # save stats to csv:
    df = pd.DataFrame({'min fitness': STATS_FITNESS_MIN,
                       'max fitness': STATS_FITNESS_MAX,
                       'average fitness': STATS_FITNESS_AVG})

    df.to_csv('stats.csv', index=False)


if __name__ == "__main__":
    main()
