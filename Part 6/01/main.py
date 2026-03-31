from Input.reading_from_input import load_students, load_examiners, load_questions, to_queue
from UI.ui import during_exam, after_exam
from Exam.exam_simulation import exam_simulation
from Shared.update_shared import update_question, update_list
from multiprocessing import Queue, Process
import time

def main():
    examiners = load_examiners()
    students = load_students()
    students_queue = to_queue(students)
    question_bank = load_questions()
    info_examiners = Queue()
    info_students = Queue()
    info_questions = Queue()

    processes = []

    for examiner in examiners:
        p = Process(
            target=exam_simulation,
            args=(examiner, students_queue, question_bank, info_examiners, info_students, info_questions)
        )

        processes.append(p)
        p.start()

    start_time = time.perf_counter()
    duration = 0
    while True:
        if any(p.is_alive() for p in processes):
            duration = time.perf_counter() - start_time
        is_sq_empty = update_list(students, info_students)
        is_eq_empty = update_list(examiners, info_examiners)
        if during_exam(examiners, students, duration) == 0 and is_sq_empty and is_eq_empty:
            break

    update_question(question_bank, info_questions)
    after_exam(examiners, students, question_bank, duration)

if __name__ == "__main__":
    main()
