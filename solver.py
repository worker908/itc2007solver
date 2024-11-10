# solver.py
from abc_phase import employed_bee_phase, onlooker_bee_phase, scout_bee_phase
from ga_phase import crossover, mutate_solution
from ifs_phase import iterative_forward_search
from utils import initialize_population
import random


def abc_ga_ifs_timetabling(problem, population_size, num_generations):
    population = initialize_population(problem, population_size)
    best_solution = None
    best_fitness = float('inf')

    for generation in range(num_generations):
        if not population:
            print("Reinitializing population due to infeasibility.")
            population = initialize_population(problem, population_size)
            employed_bee_phase(problem, population, generation, num_generations)
            onlooker_bee_phase(problem, population, generation, num_generations)
            scout_bee_phase(problem, population, generation, num_generations)

        new_population = []
        for _ in range(population_size // 2):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate_solution(child, problem, generation, num_generations)
            new_population.append(child)

        population.extend(new_population)
        population = [iterative_forward_search(sol, problem) for sol in population if
                      problem.hard_constraints_satisfied(sol)]

        if population:
            population.sort(key=lambda sol: problem.fitness(sol))
            population = population[:population_size]
            current_best_fitness = problem.fitness(population[0])

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_solution = population[0]
        else:
            print("Warning: All solutions in population are infeasible for this generation.")
            break

        print(f'Generation {generation + 1}: Best Fitness = {best_fitness}')

    return best_solution, best_fitness
