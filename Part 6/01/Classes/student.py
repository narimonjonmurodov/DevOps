import random
from .human import Human
from .question import Question

class Student(Human):
    def __init__(self, name: str, gender: str) -> None:
        super().__init__(name, gender)
        self.question: Question | None = None
        self.correct: int = 0
        self.wrong: int = 0
        self.finishing_time: float = 0
        self.status: str = "In queue"

    def take_question(self, question_bank: list[Question]) -> Question:
        self.question = random.choice(question_bank)
        return self.question
    def __str__(self):
        return str(self.name)