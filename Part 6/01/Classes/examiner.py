import random
import time
from .student import Student
from .human import Human
from multiprocessing import Queue
from .question import Question

class Examiner(Human):
    def __init__(self, name: str, gender: str) -> None:
        super().__init__(name, gender)
        self.work_time: float = 0
        self.break_time: float = 0
        self.current_student: Student | None = None
        self.total_students: int = 0
        self.failed_students: int = 0

    def status(self) -> str:
        if self.current_student is None:
            return "-"
        else:
            return str(self.current_student)

    def take_a_student(self, student_queue: Queue) -> Student:
        self.current_student = student_queue.get()
        self.total_students += 1
        return self.current_student

    def check_student_answer(self, question: Question) -> None:
        correct = set()

        while True:
            correct.add(super().chose(question.question))

            if len(correct) == len(question.question):
                break

            if random.random() > 1 / 3:
                break

        if self.current_student.chose(question.question) in correct:
            self.current_student.correct += 1
            question.sum_correct_answer()
        else:
            self.current_student.wrong += 1
        self.current_student.question = None

    def take_a_examination(self, question_bank: list[Question]) -> None:
        for _ in range(3):
            question: Question = self.current_student.take_question(question_bank)
            self.check_student_answer(question)

    def final_mark_of_student(self, start_time: float) -> None:
        r = random.random()

        if r < 1 / 8:
            self.current_student.status = "Failed"
            self.failed_students += 1

        elif r < 1 / 8 + 1 / 4:
            self.current_student.status = "Passed"

        else:
            if self.current_student.correct < self.current_student.wrong:
                self.current_student.status = "Failed"
                self.failed_students += 1
            else:
                self.current_student.status = "Passed"
        self.current_student.finishing_time = round(time.time() - start_time, 2)
        self.current_student = None

    def working(self) -> float:
        duration = round(random.uniform(len(self.name) - 1, len(self.name) + 1), 2)
        self.work_time += duration
        return duration

    def get_a_break_time(self, break_time) -> None:
        self.break_time += break_time