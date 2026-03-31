import random
from Classes.examiner import Examiner
from Classes.question import Question
from queue import Queue
import time

def update(info_students, info_examiners, current_student, examiner):
    info_students.put(current_student)
    info_examiners.put(examiner)

def exam_simulation(examiner: Examiner, students: Queue, question_bank: list[Question], info_examiners: Queue, info_students: Queue, info_questions: Queue) -> None:
    start_time: float = time.perf_counter()

    while True:
        if time.perf_counter() - start_time > 30:
            break_time = random.uniform(12, 18)
            time.sleep(break_time)
            examiner.get_a_break_time(break_time)
            start_time = time.perf_counter()
        else:
            if students.qsize() == 0:
                break
            current_student = examiner.take_a_student(students)
            info_examiners.put(examiner)
            examiner.take_a_examination(question_bank)
            duration = examiner.working()
            info_examiners.put(examiner)
            time.sleep(duration)
            examiner.final_mark_of_student(start_time)
            update(info_students, info_examiners, current_student, examiner)

        for q in question_bank:
            info_questions.put(q)

