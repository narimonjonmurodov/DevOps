from Classes.student import Student
from Classes.examiner import Examiner
from Classes.question import Question
from multiprocessing import Queue
from typing import Type, Union

def load(file_path: str, cls: Type[Union[Student, Examiner, Question]], is_question: bool = False):
    objects = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if is_question:
                objects.append(cls(line.split()))
            else:
                name, gender = line.split()
                objects.append(cls(name, gender))
                
    return objects


def to_queue(items: list[Student]) -> Queue:
    q = Queue()
    for item in items:
        q.put(item)
    return q

def load_students() -> list[Student]:
    return load("Input/students.txt", Student)

def load_examiners() -> list[Examiner]:
    return load("Input/examiners.txt", Examiner)

def load_questions() -> list[Question]:
    return load("Input/questions.txt", Question, True)