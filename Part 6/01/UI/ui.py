from UI import in_exam
from UI import end_of_exam
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def during_exam(examiners: list[in_exam.Examiner], students: list[in_exam.Student], duration: float) -> int:
    clear_screen()
    remaining_students = in_exam.show_students(students)
    in_exam.show_examiners(examiners, duration)
    print(f"Remaining in queue: {remaining_students} out of {len(students)}")
    print(f"Time since exam started: {duration:.2f}")
    return remaining_students

def after_exam(examiners: list[end_of_exam.Examiner], students: list[end_of_exam.Student], question_bank: list[end_of_exam.Question], duration: float) -> None:
    clear_screen()
    end_of_exam.show_students(students)
    end_of_exam.show_examiners(examiners)
    print(f"Time from exam start to finish: {duration:.2f}")
    end_of_exam.top_performing_students(students)
    end_of_exam.show_top_examiners(examiners)
    end_of_exam.expelled_students(students)
    end_of_exam.show_best_questions(question_bank)
    end_of_exam.result(students)



