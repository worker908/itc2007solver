import pandas as pd

# Load data (replace with actual paths)
input_file_path = 'cleaned_instance1_with_constraints_v2.xlsx'
cleaned_data = pd.ExcelFile(input_file_path)

# Parse the necessary sheets
courses_df = cleaned_data.parse("Courses")
rooms_df = cleaned_data.parse("Rooms")

# Extract course capacities and room capacities
course_capacities = dict(zip(courses_df["CourseID"], courses_df["NumStudents"]))
room_capacities = dict(zip(rooms_df["RoomID"], rooms_df["Capacity"]))

# Check each course to see if there's a room that meets its capacity requirement
for course, capacity in course_capacities.items():
    suitable_rooms = [room for room, room_capacity in room_capacities.items() if room_capacity >= capacity]
    if not suitable_rooms:
        print(f"Course {course} requires {capacity} students, but no available room can accommodate this.")
