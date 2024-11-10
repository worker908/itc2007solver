# main.py
import pandas as pd
from problem import Problem
from solver import abc_ga_ifs_timetabling


def save_timetable_to_excel(best_solution, best_fitness, problem, output_file_path):
    # Prepare timetable data for saving
    timetable_data = []
    for course, (room, period) in best_solution.items():
        day = period // problem.periods_per_day
        period_in_day = period % problem.periods_per_day
        timetable_data.append({
            "Course": course,
            "Room": room,
            "Day": day,
            "Period": period_in_day
        })

    # Create a DataFrame for the timetable
    timetable_df = pd.DataFrame(timetable_data)

    # Write to Excel
    with pd.ExcelWriter(output_file_path) as writer:
        timetable_df.to_excel(writer, sheet_name="Timetable", index=False)

        # Save fitness score as a summary in another sheet
        summary_df = pd.DataFrame({"Metric": ["Best Fitness (Penalty Score)"], "Value": [best_fitness]})
        summary_df.to_excel(writer, sheet_name="Summary", index=False)


# Load data from Excel file
input_file_path = 'cleaned_instance1_with_constraints_v2.xlsx'  # Replace with the actual file path
cleaned_data = pd.ExcelFile(input_file_path)

# Parse each sheet to use as input
parameters_df = cleaned_data.parse("Parameters")
courses_df = cleaned_data.parse("Courses")
rooms_df = cleaned_data.parse("Rooms")
curricula_df = cleaned_data.parse("Curricula")
unavailability_df = cleaned_data.parse("UnavailabilityConstraints")

# Initialize the problem instance with loaded data
problem = Problem(parameters_df, courses_df, rooms_df, curricula_df, unavailability_df)

# Run the solver
best_solution, best_fitness = abc_ga_ifs_timetabling(problem, population_size=50, num_generations=100)

# Save the timetable output to Excel
output_file_path = "final_timetable_output.xlsx"  # Replace with your desired output path
save_timetable_to_excel(best_solution, best_fitness, problem, output_file_path)
print("Timetable saved to:", output_file_path)
