from Classes.examiner import Examiner
from Classes.student import Student
from Classes.question import Question
from multiprocessing import Queue
from queue import Empty
from typing import Union

def update_list(main_list: list[Union[Student, Examiner]], out_queue: Queue) -> bool | None:
    try:
        obj = out_queue.get_nowait()

        for i in range(len(main_list)):
            if main_list[i].name == obj.name:
                main_list[i] = obj
                return False

    except Empty:
        return True


def update_question(main_list: list[Question], out_queue: Queue) -> None:
    while True:
        try:
            obj = out_queue.get_nowait()

            for q in main_list:
                if str(q) == str(obj):
                    q.correct_answer += obj.correct_answer
                    break

        except Empty:
            return