# ifs_phase.py
import random

def iterative_forward_search(solution, problem):
    for course in problem.course_capacities.keys():
        room, period = solution[course]
        if problem.course_capacities[course] > problem.room_capacities[room] or not problem.hard_constraints_satisfied(solution):
            solution[course] = (random.choice(list(problem.room_capacities.keys())), random.randint(0, problem.total_periods - 1))
    return solution
