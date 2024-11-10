# utils.py
import random


def initialize_population(problem, population_size):
    """Initialize a more constraint-aware population."""
    population = []
    attempts = 0

    while len(population) < population_size and attempts < population_size * 10:
        solution = random_solution(problem)
        if problem.hard_constraints_satisfied(solution):
            population.append(solution)
        attempts += 1

    if len(population) < population_size:
        print(f"Warning: Only {len(population)} feasible solutions generated out of {population_size} required.")

    return population


def random_solution(problem):
    """Generate a random solution that respects room capacity and unavailability constraints."""
    solution = {}
    room_periods = set()

    for course, capacity in problem.course_capacities.items():
        suitable_rooms = [room for room, room_capacity in problem.room_capacities.items() if room_capacity >= capacity]

        if suitable_rooms:
            for _ in range(10):  # Attempt to place the course up to 10 times
                room = random.choice(suitable_rooms)
                period = random.randint(0, problem.total_periods - 1)

                # Check for unavailability constraint and double booking
                day = period // problem.periods_per_day
                time_slot = period % problem.periods_per_day
                if ((course, day, time_slot) not in problem.unavailability_constraints and
                        (room, period) not in room_periods):
                    solution[course] = (room, period)
                    room_periods.add((room, period))
                    break
            else:
                solution[course] = (None, None)  # Unassigned if no valid placement found
        else:
            solution[course] = (None, None)

    return solution

def stagnation_detected(solution):
    """Placeholder function to detect stagnation in the solution."""
    # Currently returns False, meaning it does not detect stagnation.
    # You can expand this to track solution improvement across generations.
    return False