from typing import NamedTuple, Set

class Word(NamedTuple):
    text: str
    unique_letters: Set[str]

    @staticmethod
    def create(text: str):
        unique_letters = set(text)
        return Word(text, unique_letters)
