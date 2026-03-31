from Classes.question import Question
from .in_exam import show_students, Examiner, Student
from prettytable import PrettyTable

def show_examiners(examiners: list[Examiner]):
    table = PrettyTable()
    table.field_names = ["Examiner", "Total students", "Failed", "Work time"]

    for e in examiners:
        table.add_row([e.name, e.total_students, e.failed_students, f"{e.work_time:.2f}"])

    print(table)
    print()

def top_performing_students(students: list[Student]):
    passed_students = [s for s in students if s.status == "Passed"]
    if len(passed_students) == 0:
        print("Top-performing students: - ")
        return
    fastest = min(s.finishing_time for s in passed_students)
    top_students = [
        s.name for s in passed_students
        if s.finishing_time == fastest
    ]
    print("Top-performing students:", ", ".join(top_students))

def show_top_examiners(examiners: list[Examiner]):
    min_fail = min(e.failed_students for e in examiners)
    top_examiners = [
        e.name for e in examiners
        if e.failed_students == min_fail
    ]
    print("Top examiners:", ", ".join(top_examiners))

def expelled_students(students):
    failed_students = [s for s in students if s.status == "Failed"]
    if len(failed_students) == 0:
        print("Students to be expelled: - ")
        return
    earliest_fail = min(s.finishing_time for s in failed_students)
    expelled = [
        s.name for s in failed_students
        if s.finishing_time == earliest_fail
    ]
    print("Students to be expelled:", ", ".join(expelled))

def show_best_questions(question_bank: list[Question]):
    max_correct_answer = max(q.correct_answer for q in question_bank)
    if max_correct_answer == 0:
        print("Best questions: - ")
        return
    best_questions = [
        str(q) for q in question_bank
        if q.correct_answer == max_correct_answer
    ]
    print("Best questions:", ", ".join(best_questions))

def result(students: list[Student]):
    passed_count = sum(1 for s in students if s.status == "Passed")
    total = len(students)
    percentage_passed = (passed_count / total) * 100
    if percentage_passed > 85:
        print("Result: Exam successful")
    else:
        print("Result: Exam failed")