class Question:
    def __init__(self, question: list[str]):
        self.question = question
        self.question: list[str] = question
        self.correct_answer: int = 0

    def sum_correct_answer(self) -> None:
        self.correct_answer += 1

    def __str__(self) -> str:
        return " ".join(self.question)