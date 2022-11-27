import random
from typing import List
from composer_util import generate_random_note, Melody

Genome = Melody
Population = List[Melody]
FitnessVal = int
TournamentParams = dict[str]

INPUT_MELODY = None


def set_fitness_reference(input_melody: Melody):
    global INPUT_MELODY
    INPUT_MELODY = input_melody


def generate_genome(length: int) -> Melody:
    return Melody([generate_random_note() for _ in range(length)])


def play_tournament(tournament_params: TournamentParams, population: Population, worst_genome: Genome) -> List[Melody]:
    number_of_winners = tournament_params['winners']
    k = tournament_params['k']

    winner_counter = 0
    winners = []

    while winner_counter < number_of_winners:

        k_count = 0

        # Init fitness to the worst fitness in a generation
        best_genome = worst_genome

        while k_count < k:

            random_genome = random.choice(population)

            # If the picked genome has better fitness than best_genome we save it
            if random_genome.fitness < best_genome.fitness:
                best_genome = random_genome

            k_count += 1

        # Once we've gone k-times over we select
        winners.append(best_genome)

        winner_counter += 1

    return winners


def perform_crossover(population: Population, number_of_offspring: int) -> Population:
    new_population = []

    for i in range(int(number_of_offspring / 2)):

        parent_one = random.choice(population)
        parent_two = random.choice(population)

        length_matches = len(parent_one) == len(parent_two)

        # (If) Something's wrong, I can feel it
        if not length_matches:
            print('Parent genomes must be of the same length.')

            raise IndexError

        # Can't cross over a genome of size 1
        if len(parent_one) == 1:
            return population

        # Initialize offspring with new melodies
        offspring_one = Melody()
        offspring_two = Melody()

        # Generate unique cross points of which the first one is smaller
        cross_point_one = random.randint(a=0, b=len(parent_one) - 2)
        cross_point_two = random.randint(a=cross_point_one + 1, b=len(parent_one) - 1)

        # Copy first slice from corresponding parent (parent_one -> offspring_one)
        offspring_one += parent_one[:cross_point_one]
        offspring_two += parent_two[:cross_point_one]

        # Copy the middle slice from opposite parent (parent_one -> offspring_two)
        offspring_one += parent_two[cross_point_one:cross_point_two]
        offspring_two += parent_one[cross_point_one:cross_point_two]

        # Copy the last slice from corresponding parent (parent_one -> offspring_one)
        offspring_one += parent_one[cross_point_two:]
        offspring_two += parent_two[cross_point_two:]

        offspring_one.calculate_fitness(INPUT_MELODY)
        offspring_two.calculate_fitness(INPUT_MELODY)

        # Check which genome is better, and add the better to the new population
        new_population.append(offspring_one) if offspring_one.fitness >= parent_one.fitness \
            else new_population.append(parent_one)
        new_population.append(offspring_two) if offspring_two.fitness >= parent_two.fitness \
            else new_population.append(parent_two)

    return new_population


def mutate(params: dict, population: Population) -> Population:
    new_population = []

    for genome in population:
        will_mutate = random.random() <= params['chance']

        if will_mutate:

            number_of_mutations = random.randint(1, params['number_of_genes']+1)

            for _ in range(number_of_mutations):
                gene_index = random.randint(0, len(genome)-1)

                genome[gene_index] = generate_random_note()

            genome.calculate_fitness(INPUT_MELODY)

        new_population.append(genome)

    return new_population
