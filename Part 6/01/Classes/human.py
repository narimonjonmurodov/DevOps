import random

class Human:
    def __init__(self, name: str, gender: str) -> None:
        self.name: str = name
        self.gender: str = gender

    def chose(self, question: list):
        n = len(question)

        if self.gender == "M":
            weights = [n - i for i in range(n)]
        else:
            weights = [i + 1 for i in range(n)]

        return random.choices(question, weights=weights)[0]