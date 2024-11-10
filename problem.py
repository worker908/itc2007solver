# problem.py
import pandas as pd


class Problem:
    def __init__(self, parameters_df, courses_df, rooms_df, curricula_df, unavailability_df):
        # Extract basic parameters
        self.num_courses = int(parameters_df[parameters_df["Parameter"] == "Courses"]["Value"].values[0])
        self.num_rooms = int(parameters_df[parameters_df["Parameter"] == "Rooms"]["Value"].values[0])
        self.num_days = int(parameters_df[parameters_df["Parameter"] == "Days"]["Value"].values[0])
        self.periods_per_day = int(parameters_df[parameters_df["Parameter"] == "Periods_per_day"]["Value"].values[0])
        self.total_periods = self.num_days * self.periods_per_day

        # Process courses data
        self.course_capacities = dict(zip(courses_df["CourseID"], courses_df["NumStudents"]))
        self.min_days = dict(zip(courses_df["CourseID"], courses_df["MinDays"]))
        self.num_lectures = dict(zip(courses_df["CourseID"], courses_df["NumLectures"]))

        # Process room capacities
        self.room_capacities = dict(zip(rooms_df["RoomID"], rooms_df["Capacity"]))

        # Process curricula constraints
        self.curriculum_constraints = curricula_df.set_index("CurriculumID").T.to_dict(orient="list")

        # Process unavailability constraints
        self.unavailability_constraints = unavailability_df.groupby("CourseID").apply(
            lambda x: list(zip(x["Day"], x["Period"]))).to_dict()

    def hard_constraints_satisfied(self, solution):
        room_periods = {}
        for course, (room, period) in solution.items():
            if self.course_capacities[course] > self.room_capacities[room]:
                print(f"Room capacity violated for course {course} in room {room}")
                return False
            if (room, period) in room_periods:
                print(f"Double booking in room {room} at period {period}")
                return False
            room_periods[(room, period)] = course

        for curriculum, courses in self.curriculum_constraints.items():
            scheduled_periods = [solution[course][1] for course in courses if course in solution]
            if len(scheduled_periods) != len(set(scheduled_periods)):
                print(f"Curriculum conflict detected in curriculum {curriculum}")
                return False

        for course, unavailable_slots in self.unavailability_constraints.items():
            if course in solution:
                _, period = solution[course]
                day = period // self.periods_per_day
                period_in_day = period % self.periods_per_day
                if (day, period_in_day) in unavailable_slots:
                    print(
                        f"Unavailability constraint violated for course {course} on day {day}, period {period_in_day}")
                    return False

        return True

    def soft_constraints_penalty(self, solution):
        penalty = 0

        for course, (room, _) in solution.items():
            if self.course_capacities[course] > self.room_capacities[room]:
                penalty += (self.course_capacities[course] - self.room_capacities[room]) * 1

        course_days = {course: set() for course in self.num_lectures}
        for course, (_, period) in solution.items():
            day = period // self.periods_per_day
            course_days[course].add(day)

        for course, days in course_days.items():
            if len(days) < self.min_days[course]:
                penalty += (self.min_days[course] - len(days)) * 5

        for curriculum, courses in self.curriculum_constraints.items():
            for course in courses:
                if course in solution:
                    period = solution[course][1]
                    day = period // self.periods_per_day
                    day_periods = [solution[c][1] % self.periods_per_day for c in courses if
                                   c in solution and solution[c][1] // self.periods_per_day == day]
                    if len(day_periods) > 1 and max(day_periods) - min(day_periods) > 1:
                        penalty += 2

        for course in self.num_lectures:
            rooms_used = {solution[lecture][0] for lecture in self.curriculum_constraints.get(course, []) if
                          lecture in solution}
            if len(rooms_used) > 1:
                penalty += (len(rooms_used) - 1)

        return penalty

    def fitness(self, solution):
        if not self.hard_constraints_satisfied(solution):
            return float('inf')
        return self.soft_constraints_penalty(solution)
