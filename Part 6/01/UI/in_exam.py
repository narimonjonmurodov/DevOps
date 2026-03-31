from Classes.student import Student
from Classes.examiner import Examiner
from prettytable import PrettyTable

def show_students(students: list[Student]) -> int | None:
    sorted_students = sort_students(students)
    table = PrettyTable()
    table.field_names = ["Student", "Status"]
    remaining_students = 0
    for s in sorted_students:
        if s.status == "In queue":
            remaining_students += 1
        table.add_row([s.name, s.status])

    print(table)
    print()
    return remaining_students

def show_examiners(examiners: list[Examiner], duration: float) -> None:
    table = PrettyTable()
    table.field_names = ["Examiner", "Current student", "Total students", "Failed", "Work time"]

    for e in examiners:
        if e.work_time + e.break_time > duration:
            table.add_row([e.name, e.status(), e.total_students, e.failed_students, f"{duration - e.break_time:.2f}"])
        else:
            table.add_row([e.name, e.status(), e.total_students, e.failed_students, f"{e.work_time:.2f}"])

    print(table)
    print()

def sort_students(students):
    order = {
        "In queue": 0,
        "Passed": 1,
        "Failed": 2
    }
    return sorted(students, key=lambda s: order[s.status])
