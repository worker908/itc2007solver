# ga_phase.py
import random


def crossover(parent1, parent2):
    """Simple crossover that swaps random parts of two solutions."""
    child = parent1.copy()
    for course in child.keys():
        if random.random() < 0.5:
            child[course] = parent2[course]
    return child


def mutate_solution(solution, problem, generation, max_generations):
    """Mutation with an adaptive mutation rate based on generation progress."""
    mutated_solution = solution.copy()

    initial_mutation_rate = 0.1
    final_mutation_rate = 0.05
    mutation_rate = initial_mutation_rate * (1 - (generation / max_generations)) + final_mutation_rate * (
                generation / max_generations)

    for course, (room, period) in solution.items():
        if random.random() < mutation_rate:
            suitable_rooms = [room for room, cap in problem.room_capacities.items() if
                              cap >= problem.course_capacities[course]]
            if suitable_rooms:
                new_room = random.choice(suitable_rooms)
                new_period = random.randint(0, problem.total_periods - 1)

                # Only apply mutation if it avoids unavailability and double booking
                day = new_period // problem.periods_per_day
                time_slot = new_period % problem.periods_per_day
                if ((course, day, time_slot) not in problem.unavailability_constraints and
                        (new_room, new_period) not in [(r, p) for r, p in mutated_solution.values()]):
                    mutated_solution[course] = (new_room, new_period)

    return mutated_solution
