# abc_phase.py
import random
from utils import random_solution
from ga_phase import mutate_solution

def employed_bee_phase(problem, population, generation, max_generations):
    """Perform employed bee phase with mutation based on generation and max_generations."""
    for i, solution in enumerate(population):
        new_solution = mutate_solution(solution, problem, generation, max_generations)
        if problem.fitness(new_solution) < problem.fitness(solution):
            population[i] = new_solution

def onlooker_bee_phase(problem, population, generation, max_generations):
    """Perform onlooker bee phase."""
    for i, solution in enumerate(population):
        new_solution = mutate_solution(solution, problem, generation, max_generations)
        if problem.fitness(new_solution) < problem.fitness(solution):
            population[i] = new_solution

def scout_bee_phase(problem, population, generation, max_generations):
    """Scout phase with reset of solutions that fail to improve."""
    for i in range(len(population)):
        if random.random() < 0.05:  # Small probability for scout reset
            population[i] = random_solution(problem)
