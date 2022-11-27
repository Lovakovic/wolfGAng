from os import system, name
from typing import List
from improvements import play
from composer_util import set_note_gen_params, Melody
from genetic import set_fitness_reference, generate_genome, play_tournament, perform_crossover, mutate

Gene = str
Genome = Melody
Population = List[Melody]
Solution = tuple[Genome, int]

# Parameters to fiddle with
GENERATION_SIZE = 50
tournament_params = {
    'winners': int(GENERATION_SIZE / 4),
    'k': GENERATION_SIZE / 2
}
mutation_params = {
    'chance': 0.05,
    'number_of_genes': 2
}


def clear_output():
    system('cls') if name == 'nt' else system('clear')


class Composer:
    def __init__(self, melody: Melody):
        self.input_melody = melody

        # Sharing input melody with other scripts,
        # so we don't have to pass them constantly
        set_note_gen_params(melody)
        set_fitness_reference(melody)

        # Changing attributes
        self.population = None
        self.solution_found = False
        self.solution = None

    # The actual driving function for the algorithm
    def compose(self, play_frequency: int = 1, thread_number=None) -> Solution:
        generation_count = 0

        self.spawn_first_generation()

        # General loop for looping through generations
        while not self.solution_found:

            # print(f'Generation No.: {generation_count}, best fitness: {self.population[0].fitness}')

            # Check if we have a melody with a fitness of 0
            self.solution_found = sum(map(lambda melody: melody.fitness == 0, self.population))

            # Print and exit if the solution is found
            if self.solution_found:
                clear_output()
                self.solution = next(filter(lambda melody: melody.fitness == 0, self.population), None)

                return self.solution, generation_count

            # Grab the best genome in a current population
            self.population = sorted(self.population, key=lambda melody: melody.fitness)
            best_genome, worst_genome = self.population[0], self.population[-1]

            # Multithreading status output
            if thread_number is not None and generation_count % play_frequency == 0 and play_frequency > 1:
                print(f'Thread {thread_number} at generation No. {generation_count}, '
                      f'fitness: {self.population[0].fitness}')

            # Play ever n generations
            elif generation_count % play_frequency == 0 and play_frequency != 1:
                print(f'Generation No.: {generation_count}, best fitness: {self.population[0].fitness}')

                # print(f'Playing best genome: {best_genome}')
                # play(self.population[0].sounds)

            winners = play_tournament(tournament_params, self.population, worst_genome)

            # Firstly perform crossover on the population and get a brand new one
            new_population = perform_crossover(winners, GENERATION_SIZE)

            # Then mutate the new population
            self.population = mutate(mutation_params, new_population)

            generation_count += 1

    def recalculate_fitness(self):
        for genome in self.population:
            genome.calculate_fitness(self.input_melody)

    def spawn_first_generation(self):
        self.population = [generate_genome(len(self.input_melody)) for _ in range(GENERATION_SIZE)]

        self.recalculate_fitness()
